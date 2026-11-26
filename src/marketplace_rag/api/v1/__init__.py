from fastapi import APIRouter

from marketplace_rag.api.v1.gem_types import router as gem_types_router
from marketplace_rag.api.v1.shapes import router as shapes_router

api_v1_router = APIRouter()
api_v1_router.include_router(gem_types_router)
api_v1_router.include_router(shapes_router)
