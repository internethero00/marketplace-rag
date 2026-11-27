import uuid
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.core.exceptions import ConflictError, NotFoundError
from marketplace_rag.models import Shape
from marketplace_rag.repositories.shape import ShapeRepository
from marketplace_rag.schemas.shape import ShapeCreate, ShapeUpdate


class ShapeService:
    def __init__(self, session: AsyncSession, repository: ShapeRepository) -> None:
        self.session = session
        self.repository = repository

    async def list_shapes(self, include_inactive: bool) -> Sequence[Shape]:
        return await self.repository.list_all(include_inactive)

    async def get_shape(self, shape_id: uuid.UUID) -> Shape:
        shape = await self.repository.get(shape_id)
        if shape is None:
            raise NotFoundError("Shape not found")
        return shape

    async def create_shape(self, data: ShapeCreate) -> Shape:
        shape = Shape(name=data.name, icon_url=data.icon_url, is_active=data.is_active)
        self.repository.add(shape)

        await self._commit(conflict_message=f"Shape '{data.name}' already exists")
        await self.session.refresh(shape)
        return shape

    async def update_shape(self, shape_id: uuid.UUID, data: ShapeUpdate) -> Shape:
        shape = await self.get_shape(shape_id)

        changes = data.model_dump(exclude_unset=True)
        for field_name, new_value in changes.items():
            setattr(shape, field_name, new_value)

        await self._commit(conflict_message="Shape with this name already exists")
        await self.session.refresh(shape)
        return shape

    async def delete_shape(self, shape_id: uuid.UUID) -> None:
        shape = await self.get_shape(shape_id)
        await self.repository.delete(shape)
        await self._commit(conflict_message="Shape is in use and cannot be deleted")

    async def _commit(self, conflict_message: str) -> None:
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise ConflictError(conflict_message) from error
