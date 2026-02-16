from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.user import get_user_service
from app.domain.user.schemas import UserUpdate
from app.domain.user.service import UserService

from .model import User

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):

    return user


@router.patch("/me")
async def update_me(
    update_data: UserUpdate, service: UserService = Depends(get_user_service)
):

    return await service.update_user(update_data)
