import uuid
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_currency_service
from app.modules.finance.currencies.model import CurrencyType
from app.modules.finance.currencies.service import CurrencyService
from app.modules.user.model import User

from .schema import CurrencyCreate, CurrencyUpdate, CurrencyResponse

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.post("", response_model=CurrencyResponse, status_code=HTTPStatus.CREATED)
async def create_currency(
    payload: CurrencyCreate,
    service: Annotated[CurrencyService, Depends(get_currency_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload)


@router.patch("/{currency_id}", response_model=CurrencyResponse)
async def update_currency(
    currency_id: uuid.UUID,
    payload: CurrencyUpdate,
    service: Annotated[CurrencyService, Depends(get_currency_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.update(currency_id, payload)


@router.get("/{currency_id}", response_model=CurrencyResponse)
async def get_by_id(
    currency_id: uuid.UUID,
    service: Annotated[CurrencyService, Depends(get_currency_service)],
):
    return await service.get_by_id(currency_id)


@router.get("", response_model=Page[CurrencyResponse])
async def list_currencies(
    params: Annotated[Params, Depends()],
    service: Annotated[CurrencyService, Depends(get_currency_service)],
    label: Optional[str] = None,
    symbol: Optional[str] = None,
    type: Optional[CurrencyType] = None,
):
    return await service.list(label=label, symbol=symbol, type=type, params=params)
