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


async def get_supabase_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: AsyncClient = Depends(get_supabase_client),
):
    try:
        response = await supabase.auth.get_user(credentials.credentials)
        if not response or not response.user:
            raise HTTPException(status_code=401, detail="Token Inválido")

        return response.user

    except Exception:
        raise HTTPException(status_code=401, detail="Sessão expirada")


async def get_current_user(
    supabase_user=Depends(get_supabase_user),
    db: AsyncSession = Depends(get_db),
):
    user_uuid = uuid.UUID(supabase_user.id)
    user = await db.get(User, user_uuid)

    if not user:
        # Aqui o erro é claro: O token é válido, mas o usuário sumiu do DB
        raise HTTPException(status_code=404, detail="Usuário não cadastrado")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuário desativado")

    return user
