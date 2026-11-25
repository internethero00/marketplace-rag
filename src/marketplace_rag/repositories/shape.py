import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.models import Shape


class ShapeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self, include_inactive: bool) -> Sequence[Shape]:
        query = select(Shape).order_by(Shape.name)
        if not include_inactive:
            query = query.where(Shape.is_active.is_(True))

        result = await self.session.scalars(query)
        return result.all()

    async def get(self, shape_id: uuid.UUID) -> Shape | None:
        return await self.session.get(Shape, shape_id)

    def add(self, shape: Shape) -> None:
        self.session.add(shape)

    async def delete(self, shape: Shape) -> None:
        await self.session.delete(shape)
