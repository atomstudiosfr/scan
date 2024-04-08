from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import AutoCorrectionAllowedCities


async def get_allowed_countries(db: AsyncSession) -> list[str]:
    statement = select(AutoCorrectionAllowedCities.country_code)
    return await db.scalars(statement)


async def get_allowed_cities(country: str, db: AsyncSession) -> list[str]:
    statement = select(AutoCorrectionAllowedCities.city_name).where(AutoCorrectionAllowedCities.country_code == country)
    result = await db.execute(statement)
    return result.scalars().all()


async def add_allowed_country_and_city(country_name: str, city_name: str, db: AsyncSession) -> AutoCorrectionAllowedCities:
    instance = AutoCorrectionAllowedCities(
        country_code=country_name,
        city_name=city_name,
    )
    db.add(instance)
    await db.commit()
    return instance
