from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import ConfigCountryToProvider, Provider
from core.schema import ProviderSchema


async def get_provider_by_name(provider_name: str, db: AsyncSession):
    statement = select(Provider).where(Provider.provider_name == provider_name.upper())
    return await db.scalar(statement)


async def add_provider_if_not_exist(prov: ProviderSchema, db: AsyncSession):
    instance = await get_provider_by_name(prov.name, db)
    if not instance:
        prov_ins = Provider(
            provider_name=prov.name,
            max_search_bar_calls=prov.max_search_bar_calls,
            max_global_calls=prov.max_global_calls,
        )
        db.add(prov_ins)
        await db.commit()
        return prov_ins
    return instance


async def add_or_update_provider(prov: ProviderSchema, db: AsyncSession):
    instance = await get_provider_by_name(prov.name, db)
    if not instance:
        prov_ins = Provider(
            provider_name=prov.name,
            max_search_bar_calls=prov.max_search_bar_calls,
            max_global_calls=prov.max_global_calls,
        )
        db.add(prov_ins)
        await db.commit()
        return prov_ins
    else:
        prov_ins = (
            update(Provider)
            .where(Provider.provider_name == instance.provider_name)
            .values(
                {
                    Provider.provider_name: prov.name,
                    Provider.max_search_bar_calls: prov.max_search_bar_calls,
                    Provider.max_global_calls: prov.max_global_calls,
                }
            )
        )
        await db.execute(prov_ins)
        await db.commit()
        return prov_ins


async def delete_provider(provider_name: str, db: AsyncSession):
    """
    deletes ConfigCountryToProvider records corresponding to Provider and then deletes Provider
    :param provider_name:
    :param db:
    :return:
    """
    statement = (
        select(ConfigCountryToProvider.id)
        .join(Provider, Provider.provider_name == ConfigCountryToProvider.provider_name)
        .where(Provider.provider_name == provider_name)
    )
    result = await db.execute(statement)
    for config_id in result.all():
        statement = delete(ConfigCountryToProvider).where(ConfigCountryToProvider.id == config_id[0])
        await db.execute(statement)

    statement = delete(Provider).where(Provider.provider_name == provider_name)
    await db.execute(statement)
    await db.commit()
