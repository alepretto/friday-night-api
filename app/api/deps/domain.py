from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_db
from app.domain.financial_institutions.repo import FinancialInstitutionsRepo
from app.domain.financial_institutions.service import FinancialInstitutionService
from app.domain.user.repo import UserRepo
from app.domain.user.service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)):

    repo = UserRepo(db)
    return UserService(repo)


def get_financial_institution_service(db: AsyncSession = Depends(get_db)):

    repo = FinancialInstitutionsRepo(db)
    return FinancialInstitutionService(repo)
