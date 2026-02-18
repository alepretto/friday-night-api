from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_currency_service
from app.domain.currencies.service import CurrencyService
from app.domain.user.model import User

from .schema import CurrencyCreate, CurrencyResponse

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.post("", response_model=CurrencyResponse, status_code=HTTPStatus.CREATED)
async def create_currency(
    payload: CurrencyCreate,
    service: Annotated[CurrencyService, Depends(get_currency_service)],
    user: Annotated[User, Depends(get_current_user)],
):

    return await service.create_update(payload)
