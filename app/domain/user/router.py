from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user

from .model import User

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):

    return user
