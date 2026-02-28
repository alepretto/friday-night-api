import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.modules.finance.categories.exceptions import CategoryAlreadyExistis
from app.modules.finance.categories.model import Category
from app.modules.finance.subcategories.model import Subcategory


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

    async def get_by_id(self, id_category: uuid.UUID, user_id: uuid.UUID):

        query = select(Category).where(
            (Category.id == id_category) & (Category.user_id == user_id)
        )

        return await self.db.scalar(query)

    async def list_by_user(self, user_id: uuid.UUID, params: Params | None = None):

        query = select(Category).where(Category.user_id == user_id)

        return await apaginate(self.db, query, params=params)

    async def list_with_subcategories(
        self, user_id: uuid.UUID
    ) -> list[tuple[Category, list[Subcategory]]]:

        cats_result = await self.db.execute(
            select(Category).where(Category.user_id == user_id)
        )
        categories = list(cats_result.scalars().all())

        if not categories:
            return []

        cat_ids = [c.id for c in categories]
        subs_result = await self.db.execute(
            select(Subcategory).where(Subcategory.category_id.in_(cat_ids))
        )
        subcategories = subs_result.scalars().all()

        subs_by_cat: dict[uuid.UUID, list[Subcategory]] = {}
        for sub in subcategories:
            subs_by_cat.setdefault(sub.category_id, []).append(sub)

        return [(cat, subs_by_cat.get(cat.id, [])) for cat in categories]
