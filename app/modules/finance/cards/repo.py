import uuid

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.modules.finance.cards.exceptions import CardNotFound
from app.modules.finance.cards.model import Card


class CardRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, model: Card) -> Card:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def get_by_id(self, card_id: uuid.UUID, user_id: uuid.UUID) -> Card:
        query = select(Card).where((Card.id == card_id) & (Card.user_id == user_id))
        model = await self.db.scalar(query)
        if not model:
            raise CardNotFound()
        return model

    async def list_by_account(
        self,
        account_id: uuid.UUID,
        user_id: uuid.UUID,
        params: Params | None = None,
    ):
        query = (
            select(Card)
            .where((Card.account_id == account_id) & (Card.user_id == user_id))
            .order_by(Card.created_at)  # type: ignore
        )
        return await apaginate(self.db, query, params=params)

    async def delete(self, card_id: uuid.UUID, user_id: uuid.UUID) -> None:
        card = await self.get_by_id(card_id, user_id)
        await self.db.delete(card)
        await self.db.commit()
