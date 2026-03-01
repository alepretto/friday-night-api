from sqlalchemy.ext.asyncio import AsyncSession
from supabase._async.client import AsyncClient

from app.core.config import settings
from app.modules.auth.exceptions import AuthUserNotFound, SessionFiledError, TelegramUserNotLinked
from app.modules.auth.telegram import extract_telegram_id, validate_init_data
from app.modules.user.repo import UserRepo

from .schema import UserSignIn, UserSignUp


class AuthService:
    def __init__(self, supabase: AsyncClient) -> None:
        self.supabase = supabase

    async def register_new_user(self, user_data: UserSignUp):

        response = await self.supabase.auth.sign_up(
            {
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name,
                    }
                },
            }
        )

        return response.user

    async def login_user(self, login_data: UserSignIn):

        response = await self.supabase.auth.sign_in_with_password(
            {"email": login_data.email, "password": login_data.password}
        )

        session = response.session
        if not session:
            raise SessionFiledError()

        user = response.user
        if not user:
            raise AuthUserNotFound()

        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "user": user.model_dump(),
        }

    async def login_with_telegram(self, init_data: str, db: AsyncSession) -> dict:
        parsed = validate_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)
        telegram_id = extract_telegram_id(parsed)

        user = await UserRepo(db).get_by_telegram_id(telegram_id)
        if not user:
            raise TelegramUserNotLinked()

        link_response = await self.supabase.auth.admin.generate_link(
            {"type": "magiclink", "email": user.email}
        )
        hashed_token = link_response.properties.hashed_token

        auth_response = await self.supabase.auth.verify_otp(
            {"email": user.email, "token": hashed_token, "type": "magiclink"}
        )

        session = auth_response.session
        if not session:
            raise SessionFiledError()

        return {
            "access_token": session.access_token,
            "token_type": "bearer",
        }
