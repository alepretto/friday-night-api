import uuid
from typing import Optional

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.currencies.exceptions import (
    CurrencyAlreadyExists,
    CurrencyNotFound,
)

from .model import Currency, CurrencyType
from .schema import CurrencyUpdate


class CurrencyRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Currency):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise CurrencyAlreadyExists(
                label=model.label, symbol=model.symbol
            ) from None

    async def update(self, currency_id: uuid.UUID, payload: CurrencyUpdate) -> Currency:
        model = await self.get_by_id(currency_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model, key, value)
        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model
        except IntegrityError:
            await self.db.rollback()
            raise CurrencyAlreadyExists(label=model.label, symbol=model.symbol) from None

    async def get_by_id(self, currency_id: uuid.UUID) -> Currency:
        model = await self.db.get(Currency, currency_id)
        if not model:
            raise CurrencyNotFound()
        return model

    async def list(
        self,
        label: Optional[str] = None,
        symbol: Optional[str] = None,
        type: Optional[CurrencyType] = None,
        params: Optional[Params] = None,
    ):
        query = select(Currency)

        if label is not None:
            query = query.where(Currency.label.ilike(f"%{label}%"))
        if symbol is not None:
            query = query.where(Currency.symbol.ilike(f"%{symbol}%"))
        if type is not None:
            query = query.where(Currency.type == type)

        query = query.order_by(Currency.label, Currency.symbol)

        return await apaginate(self.db, query, params=params)
