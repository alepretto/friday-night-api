import uuid
from datetime import datetime
from typing import Optional

from fastapi_pagination import Params

from app.modules.finance.transactions.exceptions import (
    TransactionAccessDenied,
    TransactionNotFound,
)
from app.modules.finance.transactions.model import Transaction
from app.modules.finance.transactions.repo import TransactionRepo
from app.modules.finance.transactions.schemas import TransactionCreate
from app.modules.user.model import User


class TransactionService:
    def __init__(self, repo: TransactionRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: TransactionCreate, user: User):
        model = Transaction.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def update(self, transaction_id: uuid.UUID, payload: TransactionCreate, user: User):
        transaction = await self.repo.get_by_id(transaction_id)
        if not transaction:
            raise TransactionNotFound()

        if transaction.user_id != user.id:
            raise TransactionAccessDenied()

        updated_data = payload.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(transaction, key, value)

        return await self.repo.create_update(transaction)

    async def delete(self, transaction_id: uuid.UUID, user: User):
        transaction = await self.repo.get_by_id(transaction_id)
        if not transaction:
            raise TransactionNotFound()

        if transaction.user_id != user.id:
            raise TransactionAccessDenied()

        await self.repo.delete(transaction)

    async def list_by_account(
        self,
        account_id: uuid.UUID,
        user: User,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None,
        params: Optional[Params] = None,
    ):
        return await self.repo.list_by_account(
            account_id, user.id, date_start, date_end, params
        )
