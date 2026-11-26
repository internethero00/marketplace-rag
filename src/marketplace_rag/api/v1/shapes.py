import uuid

from fastapi import APIRouter, status

from marketplace_rag.api.deps import ShapeServiceDep
from marketplace_rag.schemas.shape import ShapeCreate, ShapeRead, ShapeUpdate

router = APIRouter(prefix="/shapes", tags=["shapes"])


@router.get("")
async def list_shapes(
    service: ShapeServiceDep,
    include_inactive: bool = False,
) -> list[ShapeRead]:
    shapes = await service.list_shapes(include_inactive)
    return [ShapeRead.model_validate(shape) for shape in shapes]


@router.get("/{shape_id}")
async def get_shape(shape_id: uuid.UUID, service: ShapeServiceDep) -> ShapeRead:
    shape = await service.get_shape(shape_id)
    return ShapeRead.model_validate(shape)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_shape(data: ShapeCreate, service: ShapeServiceDep) -> ShapeRead:
    shape = await service.create_shape(data)
    return ShapeRead.model_validate(shape)


@router.patch("/{shape_id}")
async def update_shape(
    shape_id: uuid.UUID,
    data: ShapeUpdate,
    service: ShapeServiceDep,
) -> ShapeRead:
    shape = await service.update_shape(shape_id, data)
    return ShapeRead.model_validate(shape)


@router.delete("/{shape_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shape(shape_id: uuid.UUID, service: ShapeServiceDep) -> None:
    await service.delete_shape(shape_id)
