import uuid

from fastapi_pagination import Params

from app.modules.finance.categories.service import CategoryService
from app.modules.finance.subcategories.service import SubcategoryService
from app.modules.finance.tags.exceptions import (
    TagAlreadyActive,
    TagAlreadyInactive,
    TagIntegrityError,
    TagNotFound,
)
from app.modules.user.model import User
from app.modules.finance.tags.model import Tag
from app.modules.finance.tags.repo import TagRepo
from app.modules.finance.tags.schemas import TagCreate


class TagService:
    def __init__(
        self,
        repo: TagRepo,
        category_service: CategoryService,
        subcategory_service: SubcategoryService,
    ) -> None:
        self.repo = repo

        self.category_service = category_service
        self.subcategory_service = subcategory_service

    async def create_update(self, payload: TagCreate, user: User):

        category = await self.category_service.get_by_id(payload.category_id, user)
        subcategory = await self.subcategory_service.get_by_id(payload.subcategory_id)

        if category.id != subcategory.category_id:
            raise TagIntegrityError()

        model = Tag.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def get_by_id(self, tag_id: uuid.UUID, user: User):

        tag = await self.repo.get_by_id(tag_id, user.id)
        if not tag:
            raise TagNotFound()

        return tag

    async def list_by_user(
        self, user: User, active: bool | None = None, params: Params | None = None
    ):
        tags = await self.repo.list_by_user(user.id, active, params=params)
        print(tags)
        return tags

    async def toggle_tag_state(self, active: bool, tag_id: uuid.UUID, user: User):

        tag = await self.get_by_id(tag_id, user)

        if tag.active == active:
            raise TagAlreadyActive() if active else TagAlreadyInactive()

        tag.active = active

        return await self.repo.create_update(tag)
