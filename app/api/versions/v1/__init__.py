from fastapi import APIRouter

from app.domain.accounts.router import router as account_router
from app.domain.currencies.router import router as currencies_router
from app.domain.financial_institutions.router import (
    router as financial_institutions_router,
)
from app.domain.holdings.router import router as holding_router
from app.domain.payment_methods.router import router as payment_methods_router
from app.domain.transactions.router import router as transaction_router
from app.modules.user.router import router as user_router
from app.modules.auth.router import router as auth_router

from .finance import finance_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router)
v1_router.include_router(financial_institutions_router)
v1_router.include_router(auth_router)
v1_router.include_router(account_router)
v1_router.include_router(currencies_router)
v1_router.include_router(payment_methods_router)
v1_router.include_router(transaction_router)
v1_router.include_router(holding_router)
v1_router.include_router(finance_router)
