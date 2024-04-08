from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from core.database.models import AddressCorrectionRequest, Mapping
from core.schema import AddressCorrectionRequester


async def create(data: dict, db: AsyncSession) -> AddressCorrectionRequest:
    instance = insert(AddressCorrectionRequest).values(**data).on_conflict_do_nothing()
    await db.execute(instance)
    await db.commit()
    return instance.values


async def create_or_update(data: dict, db: AsyncSession) -> AddressCorrectionRequest:
    instance = (insert(AddressCorrectionRequest)
                .values(**data)
                .on_conflict_do_update(index_elements=['parcel_id', 'share_id', 'requester'], set_=data))
    await db.execute(instance)
    await db.commit()
    return instance.values


async def bulk_insert(data_list: list[dict], db: AsyncSession) -> list[AddressCorrectionRequest]:
    instance_list = []
    for data in data_list:
        instance = (insert(AddressCorrectionRequest)
                    .values(**data)
                    .on_conflict_do_update(index_elements=['parcel_id', 'share_id', 'requester'], set_=data)
                    .returning(AddressCorrectionRequest))
        instance_list.append(await db.scalar(instance))
    await db.commit()
    return instance_list


async def update_address_correction_requests(address_correction_requests: list[AddressCorrectionRequest],
                                             output_datetime: datetime,
                                             output_message: str, db: AsyncSession) -> None:
    for request in address_correction_requests:
        request.output_datetime = output_datetime
        request.output_message_raw = output_message
        request.generated = True
    await db.commit()


async def update_sent_options(address_correction_requests: list[AddressCorrectionRequest], updated_time: datetime, db: AsyncSession):
    for request in address_correction_requests:
        request.sent = True
        request.sent_datetime = updated_time
    await db.commit()


async def count_address_correction_requests(db: AsyncSession) -> list[AddressCorrectionRequest]:
    statement = select(func.count()).select_from(AddressCorrectionRequest)
    result = await db.scalars(statement)
    return result.first()


async def get_by_share_id(share_id: str, db: AsyncSession) -> list[AddressCorrectionRequest]:
    statement = select(AddressCorrectionRequest).where(AddressCorrectionRequest.share_id == share_id)
    result = await db.scalars(statement)
    return result.all()


async def get_by_share_id_and_list_of_requesters(share_id: str, requester_list: list[AddressCorrectionRequester], db: AsyncSession) -> list[
    AddressCorrectionRequest]:
    statement = (select(AddressCorrectionRequest)
                 .where(AddressCorrectionRequest.share_id == share_id)
                 .where(AddressCorrectionRequest.requester.in_(requester_list))
                 )
    result = await db.scalars(statement)
    return result.all()


async def get_address_correction_request_not_generated(share_id: str, requester: AddressCorrectionRequester, db: AsyncSession) -> list[AddressCorrectionRequest]:
    statement = (select(AddressCorrectionRequest)
                 .where(AddressCorrectionRequest.share_id == share_id)
                 .where(AddressCorrectionRequest.requester == requester)
                 .where(AddressCorrectionRequest.generated.is_(False))
                 )
    result = await db.scalars(statement)
    return result.all()


async def get_address_correction_request_generated_but_not_sent(share_id: str, requester: AddressCorrectionRequester, db: AsyncSession) -> list[AddressCorrectionRequest]:
    statement = (select(AddressCorrectionRequest)
                 .where(AddressCorrectionRequest.share_id == share_id)
                 .where(AddressCorrectionRequest.requester == requester)
                 .where(AddressCorrectionRequest.generated.is_(True))
                 .where(AddressCorrectionRequest.sent.is_(False))
                 )
    result = await db.scalars(statement)
    return result.all()


async def get_message_with_output_message_but_not_sent(limit: int | None, db: AsyncSession) -> list[tuple[str]]:
    statement = (select(AddressCorrectionRequest.share_id, AddressCorrectionRequest.requester)
                 .where(AddressCorrectionRequest.sent.is_(False))
                 .where(AddressCorrectionRequest.generated.is_(True))
                 .limit(limit))
    result = await db.execute(statement)
    return result.all()


async def get_saved_address_without_address_correction_request_generated(limit: int | None, db: AsyncSession) -> list[tuple[str]]:
    subquery = select(Mapping.original_share_id).where(Mapping.original_share_id == AddressCorrectionRequest.share_id).scalar_subquery()

    statement = (
        select(AddressCorrectionRequest.share_id, AddressCorrectionRequest.requester)
        .where(AddressCorrectionRequest.generated.is_(False))
        .where(AddressCorrectionRequest.share_id == subquery)
        .limit(limit)
    )
    result = await db.execute(statement)
    return result.all()


async def get_saved_address_without_any_address_correction_request(limit: int | None, db: AsyncSession) -> list[str]:
    statement = (select(Mapping.original_share_id)
                 .join(AddressCorrectionRequest, AddressCorrectionRequest.share_id == Mapping.original_share_id, isouter=True)
                 .where(AddressCorrectionRequest.share_id.is_(None))
                 .limit(limit)
                 )
    result = await db.scalars(statement)
    return result.all()


async def enable_sent_flag_and_update_datetime(request: AddressCorrectionRequest, now: datetime, db: AsyncSession):
    request.sent = True
    request.output_datetime = now
    await db.commit()


async def delete_by_ids(ids: list[int], db: AsyncSession):
    statement = (delete(AddressCorrectionRequest).where(AddressCorrectionRequest.id.in_(ids)))
    result = await db.execute(statement)
    await db.commit()
    return result
