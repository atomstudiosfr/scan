from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import ProviderResult


async def save(provider_name: str, share_id: str, xml_message: str, db: AsyncSession) -> ProviderResult:
    instance = ProviderResult(provider_name=provider_name, xml_message=xml_message, share_id=share_id)
    db.add(instance)
    await db.commit()
    return instance


async def get_provider_result(provider_name: str, share_id: str, db: AsyncSession) -> ProviderResult | None:
    statement = (
        select(ProviderResult)
        .where(ProviderResult.provider_name == provider_name, ProviderResult.share_id == share_id)
        .order_by(desc(ProviderResult.creation_date))
    )
    return await db.scalar(statement)
