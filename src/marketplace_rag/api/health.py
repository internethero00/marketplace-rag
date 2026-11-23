from fastapi import APIRouter, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from marketplace_rag.api.deps import SessionDep
from marketplace_rag.schemas.health import HealthRead

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(session: SessionDep, response: Response) -> HealthRead:
    try:
        await session.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthRead(status="degraded", database="unavailable")
    return HealthRead(status="ok", database="ok")
