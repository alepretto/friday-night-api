import uuid
from typing import Optional

from fastapi_pagination import Params

from app.modules.finance.currencies.model import Currency, CurrencyType
from app.modules.finance.currencies.repo import CurrencyRepo

from .schema import CurrencyCreate


class CurrencyService:
    def __init__(self, repo: CurrencyRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: CurrencyCreate):
        model = Currency.model_validate(payload)
        return await self.repo.create_update(model)

    async def get_by_id(self, currency_id: uuid.UUID):
        return await self.repo.get_by_id(currency_id)

    async def list(
        self,
        label: Optional[str] = None,
        symbol: Optional[str] = None,
        type: Optional[CurrencyType] = None,
        params: Optional[Params] = None,
    ):
        return await self.repo.list(label=label, symbol=symbol, type=type, params=params)
