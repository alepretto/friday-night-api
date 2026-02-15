from fastapi import APIRouter, Depends

from app.api.deps.core import get_auth_service

from .schema import UserSingUp
from .service import AuthService

router = APIRouter(prefix="/auth")


@router.post("/signup")
async def signup(
    user_data: UserSingUp, service: AuthService = Depends(get_auth_service)
):

    user = await service.register_new_user(user_data)

    return {
        "message": "Usuário criado. Verifique o e-mail se necessário",
        "user": user,
    }
