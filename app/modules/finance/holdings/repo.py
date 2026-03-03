import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.finance.holdings.model import Holding
from app.modules.finance.transactions.model import Transaction


class HoldingRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Holding):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def list_by_account(self, account_id: uuid.UUID, user_id: uuid.UUID) -> list[Holding]:
        stmt = (
            select(Holding)
            .join(Transaction, Transaction.id == Holding.transaction_id)  # type: ignore[arg-type]
            .where(Transaction.account_id == account_id)  # type: ignore[arg-type]
            .where(Holding.user_id == user_id)  # type: ignore[arg-type]
            .order_by(text("holdings.created_at DESC"))
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
