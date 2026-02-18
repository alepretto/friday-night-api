from app.domain.currencies.model import Currency
from app.domain.currencies.repo import CurrencyRepo

from .schema import CurrencyCreate


class CurrencyService:
    def __init__(self, repo: CurrencyRepo) -> None:
        self.repo = repo

    async def create_update(self, payload: CurrencyCreate):

        model = Currency.model_validate(payload)
        return await self.repo.create_update(model)
