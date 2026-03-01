import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.accounts.exceptions import (
    AccountAlreadyExists,
    AccountNotFound,
)
from app.modules.finance.accounts.model import Account, AccountStatus, AccountType


class AccountRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Account):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise AccountAlreadyExists(
                user_id=model.user_id,
                institution_id=model.financial_institution_id,
                type=model.type,
                subtype=model.subtype,
            ) from None

    async def get_by_id(self, account_id: uuid.UUID, user_id: uuid.UUID) -> Account:

        query = select(Account).where(
            (Account.id == account_id) & (Account.user_id == user_id)
        )
        model = await self.db.scalar(query)
        if not model:
            raise AccountNotFound()

        return model

    async def toggle_status(
        self, account_id: uuid.UUID, user_id: uuid.UUID, new_status: AccountStatus
    ) -> Account:
        model = await self.get_by_id(account_id, user_id)
        model.status = new_status
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def list(
        self,
        user_id: uuid.UUID,
        financial_institution_id: uuid.UUID | None = None,
        status: AccountStatus | None = None,
        type: AccountType | None = None,
        params: Params | None = None,
    ):

        query = select(Account).where(Account.user_id == user_id)

        if financial_institution_id is not None:
            query = query.where(
                Account.financial_institution_id == financial_institution_id
            )

        if status is not None:
            query = query.where(Account.status == status)

        if type is not None:
            query = query.where(Account.type == type)

        query = query.order_by(Account.created_at)  # type: ignore

        return await apaginate(self.db, query, params=params)
