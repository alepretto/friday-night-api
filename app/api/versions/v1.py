from fastapi import APIRouter

from app.domain.financial_institutions.router import (
    router as financial_institutions_router,
)
from app.domain.user.router import router as user_router
from app.use_cases.auth.router import router as auth_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(financial_institutions_router)
v1_router.include_router(auth_router)
