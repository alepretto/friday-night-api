from app.domain.transactions.model import Transaction
from app.domain.transactions.repo import TransactionRepo
from app.domain.transactions.schemas import TransactionCreate
from app.domain.user.model import User


class TransactionService:
    def __init__(self, repo: TransactionRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: TransactionCreate, user: User):

        model = Transaction.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create_update(model)
