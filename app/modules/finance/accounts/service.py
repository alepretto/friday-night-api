import uuid

from fastapi_pagination import Params

from app.modules.finance.accounts.model import Account, AccountStatus, AccountType  # noqa: F401
from app.modules.finance.accounts.repo import AccountRepo
from app.modules.finance.accounts.schemas import AccountCreate
from app.modules.user.model import User


class AccountService:
    def __init__(self, repo: AccountRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: AccountCreate, user: User):

        model = Account.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)

    async def get_by_id(self, account_id: uuid.UUID, user: User) -> Account:
        return await self.repo.get_by_id(account_id, user.id)

    async def toggle_status(self, account_id: uuid.UUID, user: User, new_status: AccountStatus) -> Account:
        return await self.repo.toggle_status(account_id, user.id, new_status)

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
