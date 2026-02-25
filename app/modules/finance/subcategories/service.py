from app.domain.user.model import User
from app.modules.finance.subcategories.model import Subcategory
from app.modules.finance.subcategories.repo import SubcategoryRepo
from app.modules.finance.subcategories.schemas import SubcategoryCreate


class SubcategoryService:
    def __init__(self, repo: SubcategoryRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: SubcategoryCreate, user: User):

        model = Subcategory.model_validate(payload)
        return await self.repo.create_update(model)
