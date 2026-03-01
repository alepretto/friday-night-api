import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.modules.finance.tags.exceptions import TagAlreadyExists, TagNotFound
from app.modules.finance.tags.model import Tag


class TagRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _with_relations(self, query):
        return query.options(
            selectinload(Tag.category),  # type: ignore
            selectinload(Tag.subcategory),  # type: ignore
        )

    async def create_update(self, model: Tag):
        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)

            return model

        except IntegrityError:
            await self.db.rollback()
            raise TagAlreadyExists()

    async def update(
        self,
        tag_id: uuid.UUID,
        user_id: uuid.UUID,
        category_id: uuid.UUID,
        subcategory_id: uuid.UUID,
    ) -> Tag:
        tag = await self.get_by_id(tag_id, user_id)
        if not tag:
            raise TagNotFound()
        tag.category_id = category_id
        tag.subcategory_id = subcategory_id
        try:
            self.db.add(tag)
            await self.db.commit()
            await self.db.refresh(tag)
            return tag

        except IntegrityError:
            await self.db.rollback()
            raise TagAlreadyExists()

    async def get_by_id(self, tag_id: uuid.UUID, user_id: uuid.UUID):
        query = self._with_relations(
            select(Tag).where((Tag.id == tag_id) & (Tag.user_id == user_id))
        )
        return await self.db.scalar(query)

    async def list_by_user(
        self,
        user_id: uuid.UUID,
        active: bool | None = None,
        params: Params | None = None,
    ):
        query = self._with_relations(select(Tag).where(Tag.user_id == user_id))

        if active is not None:
            query = query.where(Tag.active == active)

        return await apaginate(self.db, query, params=params)
