from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.currencies.exceptions import CurrencyAlreadyExists

from .model import Currency


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
