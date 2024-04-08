import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Provider, CountrySearchProvider, ConfigCountryToProvider
from core.schema import CountrySearchProviderSchema


async def get_config_for_country_with_default(country_code, db: AsyncSession):
    instance = (
        select(CountrySearchProvider, Provider)
        .join(Provider, Provider.provider_name == CountrySearchProvider.provider_name)
        .where(CountrySearchProvider.country_code == country_code)
    )
    result = await db.execute(instance)
    config = result.first()
    if not config:
        instance = (
            select(CountrySearchProvider, Provider)
            .join(Provider, Provider.provider_name == CountrySearchProvider.provider_name)
            .where(CountrySearchProvider.country_code == '*')
        )
        result = await db.execute(instance)
        config = result.first()
    return config


async def get_config_for_country(country_code, db: AsyncSession):
    statement = (select(CountrySearchProvider, Provider)
                 .join(Provider, Provider.provider_name == CountrySearchProvider.provider_name)
                 .where(CountrySearchProvider.country_code == country_code)
                 )
    return await db.scalars(statement)


async def add_config(country_config: CountrySearchProviderSchema, db: AsyncSession):
    instance = CountrySearchProvider(
        country_code=country_config.country_code,
        provider_name=country_config.provider_name,
        last_updated_date=datetime.datetime.now()
    )
    db.add(instance)
    await db.commit()
    return instance


async def update_or_create_for_country(country_config: CountrySearchProviderSchema, db: AsyncSession):
    instance = await get_config_for_country(country_config.country_code, db)
    if not instance:
        return add_config(country_config, db)
    else:
        instance = (
            update(CountrySearchProvider)
            .where(CountrySearchProvider.country_code == country_config.country_code)
            .where(ConfigCountryToProvider.country_code == country_config.country_code)
            .values(
                {
                    CountrySearchProvider.country_code: country_config.country_code,
                    CountrySearchProvider.provider_name: country_config.provider_name,
                    CountrySearchProvider.last_updated_date: datetime.datetime.now()
                }
            )
        )
        await db.execute(instance)
        await db.commit()
    return instance


async def add_config_if_not_exist(country_config: CountrySearchProviderSchema, db: AsyncSession):
    instance = await get_config_for_country(country_config.country_code, db)
    if not instance:
        return await add_config(country_config, db)
