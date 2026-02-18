from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_db
from app.domain.accounts.repo import AccountRepo
from app.domain.accounts.service import AccountService
from app.domain.currencies.repo import CurrencyRepo
from app.domain.currencies.service import CurrencyService
from app.domain.financial_institutions.repo import FinancialInstitutionsRepo
from app.domain.financial_institutions.service import FinancialInstitutionService
from app.domain.payment_methods.repo import PaymentMethodRepo
from app.domain.payment_methods.service import PaymentMethodService
from app.domain.transaction_tags.repo import TransactionTagRepo
from app.domain.transaction_tags.service import TransactionTagService
from app.domain.transactions.repo import TransactionRepo
from app.domain.transactions.service import TransactionService
from app.domain.user.repo import UserRepo
from app.domain.user.service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)):

    repo = UserRepo(db)
    return UserService(repo)


def get_financial_institution_service(db: AsyncSession = Depends(get_db)):

    repo = FinancialInstitutionsRepo(db)
    return FinancialInstitutionService(repo)


def get_account_service(db: AsyncSession = Depends(get_db)):
    repo = AccountRepo(db)
    return AccountService(repo)


def get_currency_service(db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepo(db)
    return CurrencyService(repo)


def get_transaction_tag_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TransactionTagRepo(db)
    return TransactionTagService(repo)


def get_payment_method_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = PaymentMethodRepo(db)
    return PaymentMethodService(repo)


def get_transaction_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TransactionRepo(db)
    return TransactionService(repo)
