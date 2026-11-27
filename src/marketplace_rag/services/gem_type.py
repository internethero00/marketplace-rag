import uuid
from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.core.exceptions import ConflictError, NotFoundError
from marketplace_rag.models import GemColor, GemTreatment, GemType
from marketplace_rag.repositories.gem_type import GemTypeRepository
from marketplace_rag.schemas.gem_type import GemAttributeCreate, GemTypeCreate, GemTypeUpdate


class GemTypeService:
    def __init__(self, session: AsyncSession, repository: GemTypeRepository) -> None:
        self.session = session
        self.repository = repository

    async def list_gem_types(self, include_inactive: bool) -> Sequence[GemType]:
        return await self.repository.list_all(include_inactive)

    async def get_gem_type(self, gem_type_id: uuid.UUID) -> GemType:
        gem_type = await self.repository.get(gem_type_id)
        if gem_type is None:
            raise NotFoundError("Gem type not found")
        return gem_type

    async def create_gem_type(self, data: GemTypeCreate) -> GemType:
        gem_type = GemType(
            name=data.name,
            mohs_hardness=data.mohs_hardness,
            is_active=data.is_active,
            colors=[GemColor(name=color_name) for color_name in data.colors],
            treatments=[GemTreatment(name=treatment_name) for treatment_name in data.treatments],
        )
        self.repository.add(gem_type)

        await self._commit(conflict_message=f"Gem type '{data.name}' already exists")
        await self.session.refresh(gem_type)
        return gem_type

    async def update_gem_type(self, gem_type_id: uuid.UUID, data: GemTypeUpdate) -> GemType:
        gem_type = await self.get_gem_type(gem_type_id)

        changes = data.model_dump(exclude_unset=True)
        for field_name, new_value in changes.items():
            setattr(gem_type, field_name, new_value)

        await self._commit(conflict_message="Gem type with this name already exists")
        await self.session.refresh(gem_type)
        return gem_type

    async def delete_gem_type(self, gem_type_id: uuid.UUID) -> None:
        gem_type = await self.get_gem_type(gem_type_id)
        await self.repository.delete(gem_type)
        await self._commit(conflict_message="Gem type is in use and cannot be deleted")

    async def add_color(self, gem_type_id: uuid.UUID, data: GemAttributeCreate) -> GemColor:
        gem_type = await self.get_gem_type(gem_type_id)

        color = GemColor(gem_type_id=gem_type.id, name=data.name)
        self.repository.add_color(color)

        await self._commit(conflict_message=f"Color '{data.name}' already exists")
        return color

    async def delete_color(self, gem_type_id: uuid.UUID, color_id: uuid.UUID) -> None:
        color = await self.repository.get_color(gem_type_id, color_id)
        if color is None:
            raise NotFoundError("Color not found")

        await self.repository.delete_color(color)
        await self._commit(conflict_message="Color is in use and cannot be deleted")

    async def add_treatment(
        self,
        gem_type_id: uuid.UUID,
        data: GemAttributeCreate,
    ) -> GemTreatment:
        gem_type = await self.get_gem_type(gem_type_id)

        treatment = GemTreatment(gem_type_id=gem_type.id, name=data.name)
        self.repository.add_treatment(treatment)

        await self._commit(conflict_message=f"Treatment '{data.name}' already exists")
        return treatment

    async def delete_treatment(self, gem_type_id: uuid.UUID, treatment_id: uuid.UUID) -> None:
        treatment = await self.repository.get_treatment(gem_type_id, treatment_id)
        if treatment is None:
            raise NotFoundError("Treatment not found")

        await self.repository.delete_treatment(treatment)
        await self._commit(conflict_message="Treatment is in use and cannot be deleted")

    async def _commit(self, conflict_message: str) -> None:
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise ConflictError(conflict_message) from error
