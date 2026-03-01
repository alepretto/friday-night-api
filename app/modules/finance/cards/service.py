import uuid

from fastapi_pagination import Params

from app.modules.finance.cards.model import Card
from app.modules.finance.cards.repo import CardRepo
from app.modules.finance.cards.schemas import CardCreate
from app.modules.user.model import User


class CardService:
    def __init__(self, repo: CardRepo) -> None:
        self.repo = repo

    async def create(self, payload: CardCreate, user: User) -> Card:
        model = Card.model_validate(payload, update={"user_id": user.id})
        return await self.repo.create(model)

    async def get_by_id(self, card_id: uuid.UUID, user: User) -> Card:
        return await self.repo.get_by_id(card_id, user.id)

    async def list_by_account(
        self,
        account_id: uuid.UUID,
        user: User,
        params: Params | None = None,
    ):
        return await self.repo.list_by_account(account_id, user.id, params)

    async def delete(self, card_id: uuid.UUID, user: User) -> None:
        await self.repo.delete(card_id, user.id)
