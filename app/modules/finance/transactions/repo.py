from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.finance.transactions.model import Transaction


class TransactionRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Transaction):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model
