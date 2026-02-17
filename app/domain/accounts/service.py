from app.domain.accounts.model import Account
from app.domain.accounts.repo import AccountRepo
from app.domain.accounts.schemas import AccountCreate
from app.domain.user.model import User


class AccountService:
    def __init__(self, repo: AccountRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: AccountCreate, user: User):

        model = Account.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)
