import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import AddressAccess


async def insert_or_update_address_access(original_share_id: str, db: AsyncSession) -> None:
    current_date = datetime.datetime.now()
    query = insert(AddressAccess).values(original_share_id=original_share_id, last_access_date=current_date)
    instance = query.on_conflict_do_update(
        index_elements=['original_share_id'],
        set_={'last_access_date': current_date}
    )
    await db.execute(instance)
    await db.commit()
