from app.domain.financial_institutions.model import FinancialInstitutions
from app.domain.financial_institutions.repo import FinancialInstitutionsRepo
from app.domain.financial_institutions.schemas import FinancialInstitutionsCreate


class FinancialInstitutionService:
    def __init__(self, repo: FinancialInstitutionsRepo) -> None:
        self.repo = repo

    async def create_update(self, schema: FinancialInstitutionsCreate):

        model = FinancialInstitutions.model_validate(schema)
        return await self.repo.create_update(model)
