import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_transaction_service
from app.modules.finance.transactions.schemas import (
    RecentTransactionResponse,
    TransactionCreate,
    TransactionResponse,
    TransactionSummaryResponse,
)
from app.modules.finance.transactions.service import TransactionService
from app.modules.user.model import User

router = APIRouter(prefix="/transactions")


@router.get("/summary", response_model=TransactionSummaryResponse)
async def get_transaction_summary(
    date_start: datetime,
    date_end: datetime,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
    account_id: Optional[uuid.UUID] = None,
):
    return await service.get_summary(user, date_start, date_end, account_id)


@router.get("/recent", response_model=list[RecentTransactionResponse])
async def get_recent_transactions(
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(default=10, ge=1, le=50),
    account_id: Optional[uuid.UUID] = None,
):
    return await service.list_recent(user, limit, account_id)


@router.post("", response_model=TransactionResponse, status_code=HTTPStatus.CREATED)
async def create_transaction(
    payload: TransactionCreate,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: uuid.UUID,
    payload: TransactionCreate,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.update(transaction_id, payload, user)


@router.delete("/{transaction_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_transaction(
    transaction_id: uuid.UUID,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    await service.delete(transaction_id, user)
    return


@router.get("", response_model=Page[TransactionResponse])
async def list_transactions(
    account_id: uuid.UUID,
    service: Annotated[TransactionService, Depends(get_transaction_service)],
    user: Annotated[User, Depends(get_current_user)],
    params: Annotated[Params, Depends()],
    date_start: Optional[datetime] = None,
    date_end: Optional[datetime] = None,
):
    return await service.list_by_account(account_id, user, date_start, date_end, params)
