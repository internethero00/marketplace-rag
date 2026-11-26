import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from marketplace_rag.api.deps import SessionDep
from marketplace_rag.repositories.gem_type import GemTypeRepository
from marketplace_rag.schemas.gem_type import (
    GemAttributeCreate,
    GemAttributeRead,
    GemTypeCreate,
    GemTypeRead,
    GemTypeUpdate,
)
from marketplace_rag.services.gem_type import GemTypeService

router = APIRouter(prefix="/gem-types", tags=["gem types"])


def get_gem_type_repository(session: SessionDep) -> GemTypeRepository:
    return GemTypeRepository(session)


GemTypeRepositoryDep = Annotated[GemTypeRepository, Depends(get_gem_type_repository)]


def get_gem_type_service(
    session: SessionDep,
    repository: GemTypeRepositoryDep,
) -> GemTypeService:
    return GemTypeService(session, repository)


GemTypeServiceDep = Annotated[GemTypeService, Depends(get_gem_type_service)]


@router.get("")
async def list_gem_types(
    service: GemTypeServiceDep,
    include_inactive: bool = False,
) -> list[GemTypeRead]:
    gem_types = await service.list_gem_types(include_inactive)
    return [GemTypeRead.model_validate(gem_type) for gem_type in gem_types]


@router.get("/{gem_type_id}")
async def get_gem_type(gem_type_id: uuid.UUID, service: GemTypeServiceDep) -> GemTypeRead:
    gem_type = await service.get_gem_type(gem_type_id)
    return GemTypeRead.model_validate(gem_type)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_gem_type(data: GemTypeCreate, service: GemTypeServiceDep) -> GemTypeRead:
    gem_type = await service.create_gem_type(data)
    return GemTypeRead.model_validate(gem_type)


@router.patch("/{gem_type_id}")
async def update_gem_type(
    gem_type_id: uuid.UUID,
    data: GemTypeUpdate,
    service: GemTypeServiceDep,
) -> GemTypeRead:
    gem_type = await service.update_gem_type(gem_type_id, data)
    return GemTypeRead.model_validate(gem_type)


@router.delete("/{gem_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gem_type(gem_type_id: uuid.UUID, service: GemTypeServiceDep) -> None:
    await service.delete_gem_type(gem_type_id)


@router.post("/{gem_type_id}/colors", status_code=status.HTTP_201_CREATED)
async def add_color(
    gem_type_id: uuid.UUID,
    data: GemAttributeCreate,
    service: GemTypeServiceDep,
) -> GemAttributeRead:
    color = await service.add_color(gem_type_id, data)
    return GemAttributeRead.model_validate(color)


@router.delete("/{gem_type_id}/colors/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_color(
    gem_type_id: uuid.UUID,
    color_id: uuid.UUID,
    service: GemTypeServiceDep,
) -> None:
    await service.delete_color(gem_type_id, color_id)


@router.post("/{gem_type_id}/treatments", status_code=status.HTTP_201_CREATED)
async def add_treatment(
    gem_type_id: uuid.UUID,
    data: GemAttributeCreate,
    service: GemTypeServiceDep,
) -> GemAttributeRead:
    treatment = await service.add_treatment(gem_type_id, data)
    return GemAttributeRead.model_validate(treatment)


@router.delete(
    "/{gem_type_id}/treatments/{treatment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_treatment(
    gem_type_id: uuid.UUID,
    treatment_id: uuid.UUID,
    service: GemTypeServiceDep,
) -> None:
    await service.delete_treatment(gem_type_id, treatment_id)
