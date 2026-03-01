from app.core.config import settings
from app.modules.auth.telegram import extract_telegram_id, validate_init_data
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

    async def link_telegram_account(self, init_data: str, user: User) -> User:
        parsed = validate_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)
        telegram_id = extract_telegram_id(parsed)
        user.telegram_id = telegram_id
        return await self.repo.updated_user(user)
