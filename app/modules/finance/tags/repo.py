from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.finance.tags.exceptions import TagAlreadyExists
from app.modules.finance.tags.model import Tag


class TagRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_update(self, model: Tag):

        try:
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)

            return model

        except IntegrityError:
            await self.db.rollback()

            raise TagAlreadyExists()
