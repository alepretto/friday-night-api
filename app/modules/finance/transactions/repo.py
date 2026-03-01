import uuid
from datetime import datetime
from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.transactions.model import Transaction


class TransactionRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Transaction):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model

    async def list_by_account(
        self,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
        params: Optional[Params] = None,
    ):
        query = (
            select(Transaction)
            .where(
                (Transaction.account_id == account_id)
                & (Transaction.user_id == user_id)
            )
            .order_by(Transaction.date_transaction.desc())  # type: ignore
        )

        if date_start:
            query = query.where(Transaction.date_transaction >= date_start)
        if date_end:
            query = query.where(Transaction.date_transaction <= date_end)

        return await apaginate(self.db, query, params=params)
