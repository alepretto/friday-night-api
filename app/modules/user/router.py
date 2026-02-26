from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_user_service
from app.modules.user.schemas import UserUpdate
from app.modules.user.service import UserService

from .model import User

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_me(user: Annotated[User, Depends(get_current_user)]):

    return user


@router.patch("/me")
async def update_me(
    update_data: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
    user: User = Depends(get_current_user),
):

    return await service.update_user(update_data, user)


@router.delete("/me", status_code=HTTPStatus.NO_CONTENT)
async def delete_me(
    service: Annotated[UserService, Depends(get_user_service)],
    user: User = Depends(get_current_user),
):

    await service.delete(user)
