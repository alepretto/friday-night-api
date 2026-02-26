import uuid

from fastapi_pagination import Params

from app.modules.finance.accounts.model import Account, AccountStatus, AccountType
from app.modules.finance.accounts.repo import AccountRepo
from app.modules.finance.accounts.schemas import AccountCreate
from app.modules.user.model import User


class AccountService:
    def __init__(self, repo: AccountRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: AccountCreate, user: User):

        model = Account.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def list(
        self,
        user: User,
        financial_institution_id: uuid.UUID | None = None,
        status: AccountStatus | None = None,
        type: AccountType | None = None,
        params: Params | None = None,
    ):

        return await self.repo.list(
            user.id, financial_institution_id, status, type, params
        )
