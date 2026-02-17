from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_account_service
from app.domain.accounts.service import AccountService
from app.domain.user.model import User

from .schemas import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts")


@router.post("", response_model=AccountResponse)
async def create_account(
    payload: AccountCreate,
    service: AccountService = Depends(get_account_service),
    user: User = Depends(get_current_user),
):

    return await service.create_update(payload, user)
