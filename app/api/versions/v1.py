from fastapi import APIRouter

from app.domain.accounts.router import router as account_router
from app.domain.currencies.router import router as currencies_router
from app.domain.financial_institutions.router import (
    router as financial_institutions_router,
)
from app.domain.payment_methods.router import router as payment_methods_router
from app.domain.transaction_tags.router import router as tag_router
from app.domain.user.router import router as user_router
from app.use_cases.auth.router import router as auth_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(financial_institutions_router)
v1_router.include_router(auth_router)
v1_router.include_router(account_router)
v1_router.include_router(currencies_router)
v1_router.include_router(tag_router)
v1_router.include_router(payment_methods_router)
