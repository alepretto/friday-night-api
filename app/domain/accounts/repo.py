from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.exceptions import AccountAlreadyExists
from app.domain.accounts.model import Account


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
