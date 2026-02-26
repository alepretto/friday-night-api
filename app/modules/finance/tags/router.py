from http import HTTPStatus
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_tag_service
from app.modules.user.model import User
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


@router.patch("/{tag_id}/deactivate", response_model=TagBase)
async def deactivate_tag(
    tag_id: uuid.UUID,
    service: Annotated[TagService, Depends(get_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.toggle_tag_state(False, tag_id, user)


@router.patch("/{tag_id}/activate", response_model=TagBase)
async def activate_tag(
    tag_id: uuid.UUID,
    service: Annotated[TagService, Depends(get_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.toggle_tag_state(True, tag_id, user)


@router.get("/{tag_id}", response_model=TagBase)
async def get_by_id(
    tag_id: uuid.UUID,
    service: Annotated[TagService, Depends(get_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.get_by_id(tag_id, user)


@router.get("", response_model=Page[TagBase])
async def list_by_user(
    params: Annotated[Params, Depends()],
    service: Annotated[TagService, Depends(get_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
    active: bool = False,
):
    return await service.list_by_user(user, active, params)
