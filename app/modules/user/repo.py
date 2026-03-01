import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.model import User


class UserRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, id_user: uuid.UUID):

        return await self.db.get(User, id_user)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.telegram_id == telegram_id))  # type: ignore[arg-type]
        return result.scalar_one_or_none()

    async def updated_user(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User):

        await self.db.delete(user)
        await self.db.commit()
