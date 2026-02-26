from http import HTTPStatus
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_subcategory_service
from app.modules.user.model import User
from app.modules.finance.subcategories.schemas import SubcategoryBase, SubcategoryCreate
from app.modules.finance.subcategories.service import SubcategoryService

router = APIRouter(prefix="/subcategories", tags=["subcategories"])


@router.post("", status_code=HTTPStatus.CREATED, response_model=SubcategoryBase)
async def create_subcategory(
    payload: SubcategoryCreate,
    service: Annotated[SubcategoryService, Depends(get_subcategory_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)


@router.get("/{subcategory_id}", response_model=SubcategoryBase)
async def get_by_id(
    subcategory_id: uuid.UUID,
    service: Annotated[SubcategoryService, Depends(get_subcategory_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.get_by_id(subcategory_id)


@router.get("/{category_id}", response_model=Page[SubcategoryBase])
async def list_by_category(
    category_id: uuid.UUID,
    params: Annotated[Params, Depends()],
    service: Annotated[SubcategoryService, Depends(get_subcategory_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.list_by_category(category_id, params=params)
