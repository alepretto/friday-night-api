from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_auth_service

from .schema import UserSignIn, UserSignUp
from .service import AuthService

router = APIRouter(prefix="/auth")


@router.post("/signup")
async def signup(
    user_data: UserSignUp, service: Annotated[AuthService, Depends(get_auth_service)]
):

    user = await service.register_new_user(user_data)

    return {
        "message": "Usuário criado. Verifique o e-mail se necessário",
        "user": user,
    }


@router.post("/login")
async def signin(
    login_data: UserSignIn, service: Annotated[AuthService, Depends(get_auth_service)]
):

    response = await service.login_user(login_data)

    return response
