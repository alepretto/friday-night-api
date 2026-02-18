from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_transaction_tag_service
from app.domain.transaction_tags.schemas import (
    TransactionTagCreate,
    TransactionTagResponse,
)
from app.domain.transaction_tags.service import TransactionTagService
from app.domain.user.model import User

router = APIRouter(prefix="/transaction-tags", tags=["transaction-tags"])


@router.post("", response_model=TransactionTagResponse, status_code=HTTPStatus.CREATED)
async def create_transaction_tag(
    payload: TransactionTagCreate,
    service: Annotated[TransactionTagService, Depends(get_transaction_tag_service)],
    user: Annotated[User, Depends(get_current_user)],
):

    return await service.create_update(payload, user)
