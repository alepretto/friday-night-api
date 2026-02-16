import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.model import User


class UserRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, id_user: uuid.UUID):

        return await self.db.get(User, id_user)

    async def updated_user(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
