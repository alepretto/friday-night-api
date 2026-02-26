from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_tag_service
from app.domain.user.model import User
from app.modules.finance.tags.schemas import TagBase, TagCreate
from app.modules.finance.tags.service import TagService


router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", status_code=HTTPStatus.CREATED, response_model=TagBase)
async def create_tag(
    payload: TagCreate,
    service: Annotated[TagService, Depends(get_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
):

    return await service.create_update(payload, user)
