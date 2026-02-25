from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.finance.categories.exceptions import CategoryAlreadyExistis
from app.modules.finance.categories.model import Category


class CategoryRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_update(self, model: Category):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return model

        except IntegrityError:
            await self.db.rollback()

            raise CategoryAlreadyExistis(label=model.label)
