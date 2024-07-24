from sqlalchemy import desc, select, update, or_, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Address, Mapping
from core.schema import AddressSchema


async def get_tf_corrected_address_by_criteria(addr_criteria: AddressSchema, db: AsyncSession):
    """
    Getting a corrected address by criteria
    :param addr_criteria: address criteria
    :param db: database session
    :return: PY address instance
    """
    my_query = (
        select(Mapping.original_share_id, Address)
        .join(Mapping, Mapping.new_share_id == Address.share_id)
        .where(Address.country_cd == addr_criteria.country_cd)
        .where(Address.postal_cd == addr_criteria.postal_cd)
        .where(Mapping.to_delete.is_(False))
    )

    # if addr_criteria.postal_cd is not None:
    #     my_query = my_query.filter(Address.postal_cd == addr_criteria.postal_cd)
    if addr_criteria.city_nm is not None:
        my_query = my_query.where(Address.city_nm.like(f"%{addr_criteria.city_nm}%"))
    if addr_criteria.street_line1_desc is not None:
        my_query = my_query.where(Address.street_line1_desc.like(f"%{addr_criteria.street_line1_desc}%"))
    if addr_criteria.company_nm is not None:
        if addr_criteria.company_nm:
            my_query = my_query.where(Address.company_nm.like(f"%{addr_criteria.company_nm}%"))
        else:
            my_query = my_query.where(Address.company_nm == addr_criteria.company_nm)
    if addr_criteria.contact_nm is not None:
        if addr_criteria.contact_nm:
            my_query = my_query.where(Address.contact_nm.like(f"%{addr_criteria.contact_nm}%"))
        else:
            my_query = my_query.where(Address.contact_nm == addr_criteria.contact_nm)

    my_query.order_by(desc(Address.last_updated_date))
    result = await db.execute(my_query)
    return result.first()


async def get_corrected_address(original_share_id, db: AsyncSession):
    """
    Getting a corrected address by an original ShareID
    :param original_share_id: original ShareID
    :param db: database session
    :return: database "mix-address" data
    """
    statement = (select(Mapping.original_share_id, Address)
                 .join(Address, Mapping.new_share_id == Address.share_id)
                 .where(Mapping.original_share_id == original_share_id)
                 .where(Mapping.to_delete.is_(False))
                 )
    result = await db.execute(statement)
    return result.first()


async def get_corrected_address_list(original_share_id_list, db: AsyncSession):
    """
    Getting all corrected addresses for a list of original ShareID
    :param original_share_id_list: list of original ShareID
    :param db: database session
    :return: list of database "mix-address" data
    """
    statement = (select(Mapping.original_share_id, Address)
                 .join(Address, Mapping.new_share_id == Address.share_id)
                 .where(Mapping.original_share_id.in_(original_share_id_list))
                 .where(Mapping.to_delete.is_(False))
                 )
    result = await db.execute(statement)
    return result.all()


async def get_async_corrected_address_list(original_share_id_list, db: AsyncSession):
    """
    Getting all corrected addresses for a list of original ShareID
    :param original_share_id_list: list of original ShareID
    :param db: database session
    :return: list of database "mix-address" data
    """
    query = (select(Mapping.original_share_id, Address)
             .join(Address, Mapping.new_share_id == Address.share_id)
             .where(Mapping.original_share_id.in_(original_share_id_list), Mapping.to_delete.is_(False)))
    result = await db.execute(query)
    return result.all()


async def delete_address(original_share_id: str, db: AsyncSession) -> None:
    statement = update(Mapping).where(Mapping.original_share_id == original_share_id).values({Mapping.to_delete: True})
    await db.execute(statement)
    await db.commit()


async def save_address(original_share_id: str, address: AddressSchema, user_id: str, db: AsyncSession) -> (Mapping, Address):
    address_insert = (insert(Address)
                      .values({'share_id': address.share_id,
                               'street_line1_desc': address.street_line1_desc,
                               'street_line2_desc': address.street_line2_desc,
                               'street_line3_desc': address.street_line3_desc,
                               'street_line4_desc': address.street_line4_desc,
                               'city_nm': address.city_nm,
                               'postal_cd': address.postal_cd,
                               'country_cd': address.country_cd,
                               'geocode_rank': address.geocode_rank,
                               'latitude': address.latitude,
                               'longitude': address.longitude,
                               'street_number': address.street_number,
                               'street_name': address.street_name,
                               'urban_cd': address.urban_cd,
                               'state_prov_cd': address.state_prov_cd,
                               'contact_nm': address.contact_nm,
                               'company_nm': address.company_nm,
                               'phone_number': address.phone_number,
                               'street_side': address.street_side,
                               'segment_id': address.segment_id,
                               'creation_user': user_id,
                               'corrected_by': address.corrected_by,
                               'last_updated_user': user_id,
                               'correction_stop_type': address.correction_stop_type,
                               'aefs_address_type_cd': address.aefs_address_type_cd,
                               'aefs_state': address.aefs_state,
                               'aefs_raw_address_id': address.aefs_raw_address_id,
                               'aefs_geocode_rank': address.aefs_geocode_rank,
                               'aefs_latitude': address.aefs_latitude,
                               'aefs_longitude': address.aefs_longitude,
                               })
                      .on_conflict_do_update(index_elements=['share_id'],
                                             set_={'street_line1_desc': address.street_line1_desc,
                                                   'street_line2_desc': address.street_line2_desc,
                                                   'street_line3_desc': address.street_line3_desc,
                                                   'street_line4_desc': address.street_line4_desc,
                                                   'city_nm': address.city_nm,
                                                   'postal_cd': address.postal_cd,
                                                   'country_cd': address.country_cd,
                                                   'geocode_rank': address.geocode_rank,
                                                   'latitude': address.latitude,
                                                   'longitude': address.longitude,
                                                   'street_number': address.street_number,
                                                   'street_name': address.street_name,
                                                   'urban_cd': address.urban_cd,
                                                   'state_prov_cd': address.state_prov_cd,
                                                   'contact_nm': address.contact_nm,
                                                   'company_nm': address.company_nm,
                                                   'phone_number': address.phone_number,
                                                   'street_side': address.street_side,
                                                   'segment_id': address.segment_id,
                                                   'last_updated_date': address.last_updated_date,
                                                   'corrected_by': address.corrected_by,
                                                   'last_updated_user': user_id,
                                                   'correction_stop_type': address.correction_stop_type,
                                                   'aefs_address_type_cd': address.aefs_address_type_cd,
                                                   'aefs_state': address.aefs_state,
                                                   'aefs_raw_address_id': address.aefs_raw_address_id,
                                                   'aefs_geocode_rank': address.aefs_geocode_rank,
                                                   'aefs_latitude': address.aefs_latitude,
                                                   'aefs_longitude': address.aefs_longitude,
                                                   }).returning(Address))
    address_instance = await db.execute(address_insert)
    mapping_insert = (insert(Mapping)
                      .values({'original_share_id': original_share_id,
                               'new_share_id': address.share_id,
                               'creation_user': user_id,
                               'last_updated_user': user_id
                               })
                      .on_conflict_do_update(index_elements=['original_share_id'],
                                             set_={'new_share_id': address.share_id,
                                                   'last_updated_user': user_id,
                                                   'to_delete': False
                                                   })).returning(Mapping.original_share_id)
    mapping_instance = await db.execute(mapping_insert)
    await db.commit()
    return mapping_instance.scalar(), address_instance.scalar()


async def get_data_extraction(db: AsyncSession):
    """
    Getting a corrected address by data extraction
    :param db: database AsyncSession
    :return: database "get_data_extraction" data
    """

    statement = select(
        Mapping.original_share_id,
        Address.street_line1_desc,
        Address.street_line2_desc,
        Address.street_line3_desc,
        Address.street_line4_desc,
        Address.street_number,
        Address.street_name,
        Address.city_nm,
        Address.state_prov_cd,
        Address.postal_cd,
        Address.country_cd,
        Address.company_nm,
        Address.contact_nm,
        Address.phone_number,
        Address.urban_cd,
        Address.geocode_rank,
        Address.latitude,
        Address.longitude,
        Address.creation_date,
        Address.last_updated_date,
        Address.correction_stop_type,
        Address.share_id,
        Address.aefs_raw_address_id,
        Address.aefs_state,
        Address.aefs_address_type_cd,
        Address.aefs_geocode_rank,
        Address.street_side,
        Address.aefs_latitude,
        Address.aefs_longitude
    ).select_from(Mapping).join(Address)
    result = await db.execute(statement)
    return result.all()


async def get_address_without_aefs_data(limit: int = 1000, db: AsyncSession = None):
    statement = select(Address).where(Address.aefs_geocode_rank.is_(None)).limit(limit)
    result = await db.scalars(statement)
    return result.all()


async def get_address_without_street_side(limit: int = 1000, db: AsyncSession = None):
    statement = select(Address).where(Address.street_side.is_(None)).limit(limit)
    result = await db.scalars(statement)
    return result.all()


async def get_address_without_corrected_by(limit: int = 1000, db: AsyncSession = None):
    statement = select(Address).where(Address.corrected_by.is_(None)).limit(limit)
    result = await db.scalars(statement)
    return result.all()


async def get_suggested_addresses(address: AddressSchema, db: AsyncSession = None):
    statement = select(Address, ((func.similarity(Address.city_nm, address.city_nm) +
                       # func.similarity(Address.street_line1_desc, address.street_line1_desc) +
                       func.similarity(Address.company_nm, address.company_nm) +
                       # func.similarity(Address.contact_nm, address.contact_nm) +
                       func.similarity(Address.postal_cd, address.postal_cd))/3).label('sim_average')).filter(
        Address.country_cd == address.country_cd,
        or_(
            func.similarity(Address.city_nm, address.city_nm) > 0.8,
            # func.similarity(Address.street_line1_desc, address.street_line1_desc) > 0.8,
            func.similarity(Address.company_nm, address.company_nm) > 0.8,
            # func.similarity(Address.contact_nm, address.contact_nm) > 0.8,
            func.similarity(Address.postal_cd, address.postal_cd) > 0.8,
        )
    ).order_by(desc('sim_average'))


    result = await db.execute(statement)
    return result.first()
