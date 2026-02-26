from app.modules.finance.holdings.model import Holding
from app.modules.finance.holdings.repo import HoldingRepo
from app.modules.finance.holdings.schemas import HoldingCreate
from app.modules.user.model import User


class HoldingService:
    def __init__(self, repo: HoldingRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: HoldingCreate, user: User):

        model = Holding.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)
