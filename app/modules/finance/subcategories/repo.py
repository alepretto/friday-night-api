import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

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

    async def get_by_id(self, subcategory_id: uuid.UUID):
        query = select(Subcategory).where(Subcategory.id == subcategory_id)

        return await self.db.scalar(query)

    async def list_by_category(
        self, category_id: uuid.UUID, params: Params | None = None
    ):
        query = select(Subcategory).where(Subcategory.category_id == category_id)
        return await apaginate(self.db, query, params=params)
