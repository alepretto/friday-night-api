import uuid

from fastapi_pagination import Params

from app.modules.user.model import User
from app.modules.finance.tags.model import Tag
from app.modules.finance.tags.repo import TagRepo
from app.modules.finance.tags.schemas import TagCreate


class TagService:
    def __init__(self, repo: TagRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: TagCreate, user: User):

        model = Tag.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def get_by_id(self, tag_id: uuid.UUID, user: User):

        tag = await self.repo.get_by_id(tag_id, user.id)
        if not tag:
            raise

        return tag

    async def list_by_user(
        self, user: User, active: bool | None = None, params: Params | None = None
    ):
        return await self.repo.list_by_user(user.id, params=params)
