from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import ConfigCountryToProvider, Provider
from core.schema import ConfigSchema


async def get_config_list_for_country(country_code: str, db: AsyncSession):
    statement = (
        select(ConfigCountryToProvider, Provider)
        .join(Provider, Provider.provider_name == ConfigCountryToProvider.provider_name)
        .filter(ConfigCountryToProvider.country_code == country_code)
        .order_by(ConfigCountryToProvider.call_order)
    )
    result = await db.execute(statement)
    return result.all()


async def get_all_config(db: AsyncSession) -> list[ConfigCountryToProvider]:
    statement = select(ConfigCountryToProvider)
    result = await db.execute(statement)
    return result.all()


async def get_country_configured(db: AsyncSession) -> list[str]:
    statement = select(ConfigCountryToProvider.country_code)
    result = await db.execute(statement)
    return result.scalars().all()


async def get_config_list_for_provider(provider_name: str, db: AsyncSession):
    statement = (
        select(ConfigCountryToProvider)
        .filter(ConfigCountryToProvider.provider_name == provider_name)
        .order_by(ConfigCountryToProvider.call_order)
    )
    result = await db.execute(statement)
    return result.all()


async def get_config_for_country_provider(country_code: str, provider_name: str, db: AsyncSession) -> ConfigCountryToProvider:
    statement = (
        select(ConfigCountryToProvider)
        .where(ConfigCountryToProvider.country_code == country_code)
        .where(ConfigCountryToProvider.provider_name == provider_name)
    )
    result = await db.execute(statement)
    return result.one_or_none()


async def get_config_for_country_provider_by_country(country_code: str, db: AsyncSession):
    statement = (select(ConfigCountryToProvider)
                 .where(ConfigCountryToProvider.country_code == country_code)
                 )
    result = await db.execute(statement)
    return result.scalars().all()


async def delete_config(country_cd: str, provider_name: str, db: AsyncSession):
    statement = (delete(ConfigCountryToProvider)
                 .where(ConfigCountryToProvider.country_code == country_cd)
                 .where(ConfigCountryToProvider.provider_name == provider_name)
                 )
    await db.execute(statement)
    await db.commit()


async def delete_config_for_country(country_cd: str, db: AsyncSession):
    statement = delete(ConfigCountryToProvider).where(ConfigCountryToProvider.country_code == country_cd)
    await db.execute(statement)
    await db.commit()


async def add_or_update_config(config: ConfigSchema, db: AsyncSession):
    instance = await get_config_for_country_provider(config.country_code, config.provider_name, db)

    if not instance:
        return await add_config(config, db)
    else:
        instance = (
            update(ConfigCountryToProvider)
            .where(ConfigCountryToProvider.provider_name == config.provider_name)
            .where(ConfigCountryToProvider.country_code == config.country_code)
            .values(
                {
                    ConfigCountryToProvider.country_code: config.country_code,
                    ConfigCountryToProvider.provider_name: config.provider_name,
                    ConfigCountryToProvider.max_calls_per_country: config.max_calls_per_country,
                    ConfigCountryToProvider.min_geocode_rank: config.min_geocode_rank,
                    ConfigCountryToProvider.max_geocode_rank: config.max_geocode_rank,
                    ConfigCountryToProvider.call_order: config.call_order,
                }
            )
        )
        await db.execute(instance)

        await db.commit()
        return instance


async def add_config(config: ConfigSchema, db: AsyncSession) -> ConfigCountryToProvider:
    instance = ConfigCountryToProvider(
        country_code=config.country_code,
        provider_name=config.provider_name,
        max_calls_per_country=config.max_calls_per_country,
        min_geocode_rank=config.min_geocode_rank,
        max_geocode_rank=config.max_geocode_rank,
        call_order=config.call_order,
    )
    db.add(instance)
    await db.commit()
    return instance
