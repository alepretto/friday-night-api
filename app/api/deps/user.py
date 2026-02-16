from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.core import get_current_user, get_db
from app.domain.user.model import User
from app.domain.user.repo import UserRepo
from app.domain.user.service import UserService


def get_user_service(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):

    repo = UserRepo(db)
    return UserService(repo, user)
