from supabase._async.client import AsyncClient

from .schema import UserSignUp


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
