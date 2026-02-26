from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.finance.holdings.model import Holding


class HoldingRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Holding):

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
