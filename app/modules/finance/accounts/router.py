from typing import Annotated
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_account_service
from app.modules.finance.accounts.model import AccountType
from app.modules.finance.accounts.service import AccountService
from app.modules.user.model import User

from .schemas import AccountCreate, AccountResponse
from app.modules.finance.accounts.model import AccountStatus

router = APIRouter(prefix="/accounts", tags=["account"])


@router.post("", response_model=AccountResponse, status_code=HTTPStatus.CREATED)
async def create_account(
    payload: AccountCreate,
    service: Annotated[AccountService, Depends(get_account_service)],
    user: Annotated[User, Depends(get_current_user)],
):

    return await service.create_update(payload, user)


@router.patch("/{account_id}/archive", response_model=AccountResponse)
async def archive_account(
    account_id: uuid.UUID,
    service: Annotated[AccountService, Depends(get_account_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.toggle_status(account_id, user, AccountStatus.deactivate)


@router.patch("/{account_id}/activate", response_model=AccountResponse)
async def activate_account(
    account_id: uuid.UUID,
    service: Annotated[AccountService, Depends(get_account_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.toggle_status(account_id, user, AccountStatus.activate)


@router.get("", response_model=Page[AccountResponse])
async def list_accounts(
    financial_institution_id: uuid.UUID | None = None,
    status: AccountStatus | None = None,
    type: AccountType | None = None,
    service: AccountService = Depends(get_account_service),
    user: User = Depends(get_current_user),
):
    return await service.list(user, financial_institution_id, status, type)
