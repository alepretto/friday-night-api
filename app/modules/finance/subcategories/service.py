import uuid

from fastapi_pagination import Params

from app.modules.finance.subcategories.excpetions import SubcategoryNotFound
from app.modules.user.model import User
from app.modules.finance.subcategories.model import Subcategory
from app.modules.finance.subcategories.repo import SubcategoryRepo
from app.modules.finance.subcategories.schemas import SubcategoryCreate


class SubcategoryService:
    def __init__(self, repo: SubcategoryRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: SubcategoryCreate, user: User):

        model = Subcategory.model_validate(payload)
        return await self.repo.create_update(model)

    async def get_by_id(self, subcategory_id: uuid.UUID):
        subcategory = await self.repo.get_by_id(subcategory_id)

        if not subcategory:
            raise SubcategoryNotFound()

        return subcategory

    async def list_by_category(
        self, category_id: uuid.UUID, params: Params | None = None
    ):

        return await self.repo.list_by_category(category_id, params)
