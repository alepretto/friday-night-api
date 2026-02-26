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
