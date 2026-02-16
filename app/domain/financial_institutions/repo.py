from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.financial_institutions.model import (
    FinancialInstitutions,
)


class FinancialInstitutionsRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: FinancialInstitutions):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model
