from app.modules.user.model import User
from app.modules.user.repo import UserRepo
from app.modules.user.schemas import UserUpdate


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def update_user(self, user_info: UserUpdate, user: User):

        infos = user_info.model_dump(exclude_unset=True)
        for info, value in infos.items():
            setattr(user, info, value)

        return await self.repo.updated_user(user)

    async def delete(self, user: User):
        await self.repo.delete_user(user)
