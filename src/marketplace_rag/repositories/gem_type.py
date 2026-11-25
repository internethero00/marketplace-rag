import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.models import GemColor, GemTreatment, GemType


class GemTypeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self, include_inactive: bool) -> Sequence[GemType]:
        query = select(GemType).order_by(GemType.name)
        if not include_inactive:
            query = query.where(GemType.is_active.is_(True))

        result = await self.session.scalars(query)
        return result.all()

    async def get(self, gem_type_id: uuid.UUID) -> GemType | None:
        return await self.session.get(GemType, gem_type_id)

    def add(self, gem_type: GemType) -> None:
        self.session.add(gem_type)

    async def delete(self, gem_type: GemType) -> None:
        await self.session.delete(gem_type)

    async def get_color(self, gem_type_id: uuid.UUID, color_id: uuid.UUID) -> GemColor | None:
        query = select(GemColor).where(
            GemColor.id == color_id,
            GemColor.gem_type_id == gem_type_id,
        )
        return await self.session.scalar(query)

    def add_color(self, color: GemColor) -> None:
        self.session.add(color)

    async def delete_color(self, color: GemColor) -> None:
        await self.session.delete(color)

    async def get_treatment(
        self,
        gem_type_id: uuid.UUID,
        treatment_id: uuid.UUID,
    ) -> GemTreatment | None:
        query = select(GemTreatment).where(
            GemTreatment.id == treatment_id,
            GemTreatment.gem_type_id == gem_type_id,
        )
        return await self.session.scalar(query)

    def add_treatment(self, treatment: GemTreatment) -> None:
        self.session.add(treatment)

    async def delete_treatment(self, treatment: GemTreatment) -> None:
        await self.session.delete(treatment)
