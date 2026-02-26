import uuid

from fastapi_pagination import Params

from app.modules.finance.categories.exceptions import CategoryNotFound
from app.modules.finance.categories.model import Category
from app.modules.finance.categories.repo import CategoryRepo
from app.modules.finance.categories.schemas import CategoryCreate
from app.modules.user.model import User


class CategoryService:
    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def create_update(self, schema: CategoryCreate, user: User):

        model = Category.model_validate(schema, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def get_by_id(self, id_category: uuid.UUID, user: User):

        category = await self.repo.get_by_id(id_category, user.id)

        if not category:
            raise CategoryNotFound()

        return category

    async def list_by_user(self, user: User, params: Params | None = None):

        return await self.repo.list_by_user(user.id, params=params)
