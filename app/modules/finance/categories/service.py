from app.modules.finance.categories.model import Category
from app.modules.finance.categories.repo import CategoryRepo
from app.modules.finance.categories.schemas import CategoryCreate
from app.domain.user.model import User


class CategoryService:
    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def create_update(self, schema: CategoryCreate, user: User):

        model = Category.model_validate(schema, update={"user_id": user.id})
        return await self.repo.create_update(model)
