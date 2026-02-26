from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
