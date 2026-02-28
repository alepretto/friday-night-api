import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.payment_methods.exceptions import PaymentMethodAlreadyExists
from app.modules.finance.payment_methods.model import PaymentMethod


class PaymentMethodRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_updated(self, model: PaymentMethod):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise PaymentMethodAlreadyExists(label=model.label) from None

    async def get_by_id(self, payment_method_id: uuid.UUID, user_id: uuid.UUID):

        query = select(PaymentMethod).where(
            (PaymentMethod.id == payment_method_id) & (PaymentMethod.user_id == user_id)
        )

        return await self.db.scalar(query)

    async def list_by_user(
        self,
        user_id: uuid.UUID,
        params: Params | None = None,
        active: bool | None = None,
    ):

        query = select(PaymentMethod).where(PaymentMethod.user_id == user_id)

        if active is not None:
            query.where(PaymentMethod.is_active == active)

        return await apaginate(self.db, query, params=params)
