import csv

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.controllers import (
    address_controller,
    package_controller, aefs_controller,
)
from api.controllers.address_controller import (
    checking_corrected_address,
    integrate_address_line_from_csv,
    is_valid_share_ids, checking_multiple_corrected_address, rule_specific_for_country,
)
from api.controllers.aefs_controller import (
    get_validated_address_from_aefs,
    get_addr_from_aefs_without_raising_error,
)
from api.controllers.authentication_controller import (
    UserDep,
    verify_can_edit, check_authentication,
)
from api.controllers.location_controller import LocationDep
from api.controllers.provider_controller import is_calling_provider_allowed
from core.db import dbDep, get_db
from core.exceptions import NoCorrectedAddressFound
from api.redis import redisDep, get_redis
from core.schema import AddressMixSchema, AddressSchema, ProviderEnum, \
    AddressMixSchemaWithMissing
from api.utils import parse_list
from worker.celery_worker import app

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    dependencies=[Depends(check_authentication)],
)

DCT_MANDATORY_FLD_PER_COUNTRY = {
    "FR": ["country_nm", "country_cd", "postal_cd", "city_nm", "street_line1_desc", "latitude", "longitude"],
    "*": ["country_nm", "country_cd", "city_nm", "street_line1_desc", "latitude", "longitude"],
}


@router.post("/check")
async def check_address_is_valid(address: AddressSchema, db: dbDep, redis: redisDep) -> AddressSchema | None:
    if await is_calling_provider_allowed(ProviderEnum.AEFS, db, redis):
        return await get_validated_address_from_aefs(address, redis)
    else:
        return None


@router.post("/update")
async def update_address(corrected_address: AddressSchema, original_address: AddressSchema,
                         location: LocationDep, db: dbDep, redis: redisDep, user: UserDep) -> AddressSchema:
    """
    Saving the corrected address for an original ShareID
    :param location : location_cd
    :param original_address: Customer address to correct
    :param corrected_address: Corrected address entered by user to update the Customer address
    :param db: database session
    :param redis: redis session
    :param user: connected user
    :return:
    """
    await verify_can_edit(user, corrected_address.country_cd, location)
    corrected_address = await checking_corrected_address(corrected_address, original_address, db, redis)
    corrected_address.geocode_rank = 50  # Manual geocode rank
    corrected_address.corrected_by = ProviderEnum.USER
    save_result = await address_controller.save(original_address, corrected_address, user.user_id, db)
    app.send_task('worker.tasks.notification.notify_all_requesters', kwargs={'share_id': original_address.share_id}, queue='notify')
    return save_result


@router.post("/update_as_one")
async def update_address_as_one(
        corrected_address: AddressSchema,
        original_address_list: list[AddressSchema],
        location: LocationDep,
        db: dbDep,
        redis: redisDep,
        user: UserDep,
) -> AddressSchema:
    """
    Saving as one the corrected address for an original ShareID (REF) and its linked original ShareIDs
    :param corrected_address: the correction
    :param original_address_list : the list of original address that need to be saved
    :param location: location attached
    :param db: database session
    :param redis: redis session
    :param user: connected user
    :return:
    """
    await verify_can_edit(user, corrected_address.country_cd, location)
    corrected_address.geocode_rank = 50  # Manual geocode rank
    corrected_address.corrected_by = ProviderEnum.USER

    await checking_multiple_corrected_address(corrected_address, original_address_list, db, redis)
    await address_controller.save_multiple_addresses(corrected_address, original_address_list, user.user_id, db)
    for original_address in original_address_list:
        app.send_task('worker.tasks.notification.notify_all_requesters', kwargs={'share_id': original_address.share_id}, queue='notify')
    return corrected_address


@router.get("/mandatory_fields/{country_cd}")
async def get_address_mandatory_fields(country_cd: str):
    """
    Mandatory core address details for general EU: Country, City, Street, House number.
    Not mandatory fields: Company name, Contact name.
    Postal code and State/province being mandatory or not depends on the country.
    check country code exists ? LSSI ? (getCountryRegions
    :param country_cd:
    :return:
    """
    return {'mandatory_fields': DCT_MANDATORY_FLD_PER_COUNTRY.get(country_cd.upper(), DCT_MANDATORY_FLD_PER_COUNTRY["*"]),
            'specific_rule': rule_specific_for_country(country_cd)}


@router.get("/get_corrected/{original_share_id}")
async def get_corrected_address(original_share_id: str, db: dbDep):
    """
    Getting the corrected address for the given original share ID
    :param original_share_id:
    :param db:
    :return:
    """
    response = await address_controller.get_corrected_address(original_share_id, db)
    if not response:
        raise NoCorrectedAddressFound()
    return response


@router.get("/get_corrected_list")
async def get_corrected_address_list(
        original_share_id_list: list[str] = Depends(parse_list(query=Query([], alias="share_id_list", description=""), class_type=str)),
        db: AsyncSession = Depends(get_db),
):
    """
    Getting corrected addresses for the given original share ID list
    :param original_share_id_list:
    :param db:
    :return:
    """
    if original_share_id_list is not None:
        response = await address_controller.get_tf_corrected_address_list(original_share_id_list, db)
        if not response:
            raise NoCorrectedAddressFound()
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/get_mix_list/")
async def get_address_mix_list(
        input_list: list[str] = Depends(parse_list(query=Query([], alias="input_value", description=""), class_type=str)),
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis)
) -> AddressMixSchemaWithMissing:
    """
    Getting Mix(Original+Corrected) addresses for the given input list (AWB/TrackingID list OR original ShareID list)
    :param input_list: input value list (AWB/TrackingID list OR original ShareID list)
    :param db: database
    :param redis: redis
    :return: List[AddressMix]
    """
    if not input_list:
        raise HTTPException(status_code=404, detail="Missing value")
    elif package_controller.is_valid_tracking_ids(input_list):
        original_address_list_return = await package_controller.get_address_from_packages(input_list)
        lst_missing_input_return = []
        lst_share_id = []
        original_address_list = []
        for o_addr in original_address_list_return:
            if not o_addr.share_id:
                # Package found in KAPI but no address linked to it
                lst_missing_input_return.append(o_addr.tracking_id)
            else:
                try:
                    input_list.remove(o_addr.tracking_id)
                except:
                    pass
                if not o_addr.share_id in lst_share_id:
                    lst_share_id.append(o_addr.share_id)
                    original_address_list.append(o_addr)
        lst_missing_input_return += input_list
    elif is_valid_share_ids(input_list):
        original_address_list = await aefs_controller.get_addresses(input_list, redis)
        for address in original_address_list:
            if address.share_id in input_list:
                input_list.remove(address.share_id)
        lst_missing_input_return = input_list
    else:
        raise HTTPException(status_code=404, detail="Input values should be either ShareId or AWB not both")

    lst_original_share_id = list(set([o_addr.share_id for o_addr in original_address_list]))
    dct_corrected_address = await address_controller.get_tf_corrected_address_list(lst_original_share_id, db)
    return AddressMixSchemaWithMissing(
        lst_address_mix_schema=[
            AddressMixSchema(original=o_addr, corrected=dct_corrected_address.get(o_addr.share_id)) for o_addr in
            original_address_list if o_addr.share_id],
        lst_missing=lst_missing_input_return
    )


@router.post("/upload_US")
async def upload_addresses(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis)
):
    if file.filename.find('.csv'):
        contents = await file.read()
        reader = csv.reader(contents.decode('utf-8').splitlines())
        data_in_error = []
        data_good = []
        count = 0
        for row in reader:
            if row[0] != 'LOCATION_CD':
                if await is_calling_provider_allowed(ProviderEnum.AEFS, db, redis):
                    aefs_address = await get_addr_from_aefs_without_raising_error(row[2], redis)
                    if aefs_address:
                        data_good.append(row)
                        await integrate_address_line_from_csv(row[1], aefs_address, db)
                        count += 1
                else:
                    data_in_error.append(row)
        return data_in_error
    else:
        raise HTTPException(status_code=415, detail="this is not a CSV File")


@router.post("/upload_CA")
async def upload_addresses(
        address_csv_file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    if address_csv_file.filename.find('.csv'):
        contents = await address_csv_file.read()

        data_in_error = []
        data_good = []
        count = 0
        reader = csv.reader(contents.decode('latin-1').splitlines())

        for row in reader:
            if row[0] != 'SHARE_ID':
                address_csv = address_controller.create_data_from_csv_ca(row)
                if address_csv:
                    data_good.append(row)
                    await integrate_address_line_from_csv(row[0], address_csv, db)
                    count += 1

        return data_in_error
    else:
        raise HTTPException(status_code=415, detail="this is not a CSV File")


@router.delete("/{shareid}")
async def delete_address_by_original_shareid(shareid: str, db: AsyncSession = Depends(get_db)):
    is_deleted = await address_controller.delete_address(shareid, db)
    if not is_deleted:
        raise NoCorrectedAddressFound()
    return is_deleted
