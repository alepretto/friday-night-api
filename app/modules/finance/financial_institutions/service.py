import uuid

from fastapi_pagination import Params

from app.modules.finance.financial_institutions.model import (
    FinancialInstitution,
    InstitutionType,
)
from app.modules.finance.financial_institutions.repo import FinancialInstitutionsRepo
from app.modules.finance.financial_institutions.schemas import (
    FinancialInstitutionCreate,
)


class FinancialInstitutionService:
    def __init__(self, repo: FinancialInstitutionsRepo) -> None:
        self.repo = repo

    async def create_update(self, schema: FinancialInstitutionCreate):

        model = FinancialInstitution.model_validate(schema)
        return await self.repo.create_update(model)

    async def get_by_id(self, institution_id: uuid.UUID):
        return await self.repo.get_by_id(institution_id)

    async def list(
        self, type: InstitutionType | None = None, params: Params | None = None
    ):

        return await self.repo.list(type=type, params=params)
