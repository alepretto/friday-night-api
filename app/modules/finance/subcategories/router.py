from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

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
