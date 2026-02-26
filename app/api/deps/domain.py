from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_db


from app.domain.holdings.repo import HoldingRepo
from app.domain.holdings.service import HoldingService


from app.modules.user.repo import UserRepo
from app.modules.user.service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)):

    repo = UserRepo(db)
    return UserService(repo)


def get_holding_service(db: Annotated[AsyncSession, Depends(get_db)]):
    repo = HoldingRepo(db)
    return HoldingService(repo)
