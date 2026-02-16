from fastapi_pagination import Params

from app.domain.financial_institutions.model import (
    FinancialInstitutions,
    InstitutionType,
)
from app.domain.financial_institutions.repo import FinancialInstitutionsRepo
from app.domain.financial_institutions.schemas import FinancialInstitutionCreate


class FinancialInstitutionService:
    def __init__(self, repo: FinancialInstitutionsRepo) -> None:
        self.repo = repo

    async def create_update(self, schema: FinancialInstitutionCreate):

        model = FinancialInstitutions.model_validate(schema)
        return await self.repo.create_update(model)

    async def list(
        self, type: InstitutionType | None = None, params: Params | None = None
    ):

        return await self.repo.list(type=type, params=params)
