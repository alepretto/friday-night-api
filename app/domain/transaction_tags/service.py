from app.domain.transaction_tags.model import TransactionTag
from app.domain.transaction_tags.repo import TransactionTagRepo
from app.domain.transaction_tags.schemas import TransactionTagCreate
from app.domain.user.model import User


class TransactionTagService:
    def __init__(self, repo: TransactionTagRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: TransactionTagCreate, user: User):

        model = TransactionTag.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)
