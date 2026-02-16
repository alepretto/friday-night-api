import uuid

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from supabase._async.client import AsyncClient, create_client

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.domain.user.model import User
from app.use_cases.auth.service import AuthService


async def get_supabase_client():
    supabase: AsyncClient = await create_client(
        settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
    )
    return supabase


async def get_auth_service(supabase: AsyncClient = Depends(get_supabase_client)):
    return AuthService(supabase)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: AsyncClient = Depends(get_supabase_client),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    try:
        response = await supabase.auth.get_user(token)
        if not response or not response.user:
            raise ValueError("Usuário não encontrado no token")

        user_uuid = uuid.UUID(response.user.id)

        user = await db.get(User, user_uuid)

        if not user:
            raise ValueError("Usuário não encontrado no Banco de dados")

        return user

    except Exception as e:
        print(f"Erro crítico capturado: {e}")
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
