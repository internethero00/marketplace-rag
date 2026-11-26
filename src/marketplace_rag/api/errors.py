from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from marketplace_rag.core.exceptions import ConflictError, NotFoundError


async def handle_not_found(_request: Request, error: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(error)})


async def handle_conflict(_request: Request, error: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(error)})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, handle_not_found)
    app.add_exception_handler(ConflictError, handle_conflict)
