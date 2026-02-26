from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_category_service
from app.modules.finance.categories.schemas import CategoryBase, CategoryCreate
from app.modules.finance.categories.service import CategoryService
from app.modules.user.model import User


router = APIRouter(prefix="/categories", tags=["cateogires"])


@router.post("", status_code=HTTPStatus.CREATED, response_model=CategoryBase)
async def create_category(
    payload: CategoryCreate,
    service: Annotated[CategoryService, Depends(get_category_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)
