from fastapi import Depends
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
