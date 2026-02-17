import uuid

from fastapi_pagination import Params

from app.domain.accounts.model import Account, AccountType
from app.domain.accounts.repo import AccountRepo
from app.domain.accounts.schemas import AccountCreate
from app.domain.user.model import User


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
        status: AccountType | None = None,
        type: str | None = None,
        params: Params | None = None,
    ):

        return await self.repo.list(
            user.id, financial_institution_id, status, type, params
        )
