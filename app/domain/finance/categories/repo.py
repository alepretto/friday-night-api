from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.finance.categories.model import Category


class CategoryRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_update(self, model: Category):

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
