from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from marketplace_rag.db.session import get_session
from marketplace_rag.repositories.gem_type import GemTypeRepository
from marketplace_rag.repositories.shape import ShapeRepository
from marketplace_rag.services.gem_type import GemTypeService
from marketplace_rag.services.shape import ShapeService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_gem_type_repository(session: SessionDep) -> GemTypeRepository:
    return GemTypeRepository(session)


GemTypeRepositoryDep = Annotated[GemTypeRepository, Depends(get_gem_type_repository)]


def get_gem_type_service(
    session: SessionDep,
    repository: GemTypeRepositoryDep,
) -> GemTypeService:
    return GemTypeService(session, repository)


GemTypeServiceDep = Annotated[GemTypeService, Depends(get_gem_type_service)]


def get_shape_repository(session: SessionDep) -> ShapeRepository:
    return ShapeRepository(session)


ShapeRepositoryDep = Annotated[ShapeRepository, Depends(get_shape_repository)]


def get_shape_service(
    session: SessionDep,
    repository: ShapeRepositoryDep,
) -> ShapeService:
    return ShapeService(session, repository)


ShapeServiceDep = Annotated[ShapeService, Depends(get_shape_service)]
