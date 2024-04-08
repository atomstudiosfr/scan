from sqlalchemy import func, text, or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Address


async def most_active_user(db: AsyncSession):
    statement = select(
        Address.creation_user,
        Address.last_updated_user,
        func.count().label("active_count")
    ).where(
        or_(
            Address.creation_date >= func.current_timestamp() - text("INTERVAL '7 DAY'"),
            Address.last_updated_date >= func.current_timestamp() - text("INTERVAL '7 DAY'")
        )
    ).group_by(
        Address.creation_user,
        Address.last_updated_user
    ).order_by(func.count().desc()).limit(10)

    return await db.scalars(statement)


async def country_correction_counts(db: AsyncSession):
    query = (select(Address.country_cd, func.count().label("correction_count"))
             .group_by(Address.country_cd)
             .order_by(func.count().desc()))
    return await db.scalars(query)


async def get_correction_count_by_country(country_cd: str, db: AsyncSession) -> int:
    query = select(func.count().label("correction_count")).where(Address.country_cd == country_cd)
    return await db.scalar(query)
