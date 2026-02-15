from fastapi import APIRouter

from app.api.versions.v1 import v1_router

main_router = APIRouter(prefix="/api")


main_router.include_router(v1_router)
