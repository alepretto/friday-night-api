from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_db

from app.modules.finance.categories.repo import CategoryRepo
from app.modules.finance.categories.service import CategoryService
from app.modules.finance.subcategories.repo import SubcategoryRepo
from app.modules.finance.subcategories.service import SubcategoryService
from app.modules.finance.tags.repo import TagRepo
from app.modules.finance.tags.service import TagService
from app.modules.finance.accounts.repo import AccountRepo
from app.modules.finance.accounts.service import AccountService
from app.modules.finance.currencies.repo import CurrencyRepo
from app.modules.finance.currencies.service import CurrencyService
from app.modules.finance.financial_institutions.repo import FinancialInstitutionsRepo
from app.modules.finance.financial_institutions.service import (
    FinancialInstitutionService,
)
from app.modules.finance.transactions.repo import TransactionRepo
from app.modules.finance.transactions.service import TransactionService
from app.modules.finance.payment_methods.repo import PaymentMethodRepo
from app.modules.finance.payment_methods.service import PaymentMethodService


def get_category_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = CategoryRepo(db)
    return CategoryService(repo)


def get_subcategory_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = SubcategoryRepo(db)
    return SubcategoryService(repo)


def get_tag_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TagRepo(db)
    return TagService(repo)


def get_account_service(db: AsyncSession = Depends(get_db)):
    repo = AccountRepo(db)
    return AccountService(repo)


def get_currency_service(db: AsyncSession = Depends(get_db)):
    repo = CurrencyRepo(db)
    return CurrencyService(repo)


def get_financial_institution_service(db: AsyncSession = Depends(get_db)):

    repo = FinancialInstitutionsRepo(db)
    return FinancialInstitutionService(repo)


def get_transaction_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = TransactionRepo(db)
    return TransactionService(repo)


def get_payment_method_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = PaymentMethodRepo(db)
    return PaymentMethodService(repo)
