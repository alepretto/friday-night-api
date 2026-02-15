from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase._async.client import AsyncClient, create_client

from app.core.config import settings
from app.use_cases.auth.service import AuthService


async def get_supabase_client():
    supabase: AsyncClient = await create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    return supabase


async def get_auth_service(supabase: AsyncClient = Depends(get_supabase_client)):
    return AuthService(supabase)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: AsyncClient = Depends(get_supabase_client),
):
    token = credentials.credentials
    try:
        response = await supabase.auth.get_user(token)

        if not response or not response.user:
            raise ValueError("Usuário não encontrado no token")

        return response.user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
