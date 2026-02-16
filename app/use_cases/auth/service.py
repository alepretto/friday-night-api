from supabase._async.client import AsyncClient

from app.use_cases.auth.exceptions import AuthUserNotFound, SessionFiledError

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
