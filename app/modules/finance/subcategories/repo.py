from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.finance.subcategories.excpetions import SubcategoryAlreadyExists
from app.modules.finance.subcategories.model import Subcategory


class SubcategoryRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Subcategory):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)

            return model

        except IntegrityError:
            await self.db.rollback()

            raise SubcategoryAlreadyExists(label=model.label)
