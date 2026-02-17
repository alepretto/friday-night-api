import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_account_service
from app.domain.accounts.model import AccountStatus, AccountType
from app.domain.accounts.service import AccountService
from app.domain.user.model import User

from .schemas import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["account"])


@router.post("", response_model=AccountResponse, status_code=HTTPStatus.CREATED)
async def create_account(
    payload: AccountCreate,
    service: AccountService = Depends(get_account_service),
    user: User = Depends(get_current_user),
):

    return await service.create_update(payload, user)


@router.get("", response_model=Page[AccountResponse])
async def list_accounts(
    financial_institution_id: uuid.UUID | None = None,
    status: AccountStatus | None = None,
    type: AccountType | None = None,
    service: AccountService = Depends(get_account_service),
    user: User = Depends(get_current_user),
):
    return await service.list(user, financial_institution_id, status, type)
