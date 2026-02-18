from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.transaction_tags.exceptions import TagAlreadExists
from app.domain.transaction_tags.model import TransactionTag


class TransactionTagRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: TransactionTag):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise TagAlreadExists(
                category=model.category, subcategory=model.subcategory, type=model.type
            ) from None
