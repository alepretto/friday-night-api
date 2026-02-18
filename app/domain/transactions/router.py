from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_transaction_service
from app.domain.transactions.schemas import TransactionCreate, TransactionResponse
from app.domain.transactions.service import TransactionService
from app.domain.user.model import User

router = APIRouter(prefix="/transactions")


@router.post("", response_model=TransactionResponse, status_code=HTTPStatus.CREATED)
async def create_transaction(
    payload: TransactionCreate,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)
