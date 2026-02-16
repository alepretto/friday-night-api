import uuid

from app.domain.user.exceptions import UserNotFoundError
from app.domain.user.model import User
from app.domain.user.repo import UserRepo
from app.domain.user.schemas import UserUpdate


class UserService:
    def __init__(self, repo: UserRepo, user: User) -> None:
        self.repo = repo
        self.user = user

    async def update_user(self, user_info: UserUpdate):

        infos = user_info.model_dump(exclude_unset=True)
        for info, value in infos.items():
            setattr(self.user, info, value)

        return await self.repo.updated_user(self.user)
