from http import HTTPStatus
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_payment_method_service
from app.modules.finance.payment_methods.schemas import (
    PaymentMethodCreate,
    PaymentMethodResponse,
)
from app.modules.finance.payment_methods.service import PaymentMethodService
from app.modules.user.model import User

router = APIRouter(prefix="/payment-methods", tags=["payment-methods"])


@router.post("", response_model=PaymentMethodResponse, status_code=HTTPStatus.CREATED)
async def create_payment_methods(
    payload: PaymentMethodCreate,
    service: Annotated[PaymentMethodService, Depends(get_payment_method_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)


@router.get("/{payment_method_id}", response_model=PaymentMethodResponse)
async def get_by_id(
    payment_method_id: uuid.UUID,
    service: Annotated[PaymentMethodService, Depends(get_payment_method_service)],
    user: Annotated[User, Depends(get_current_user)],
):

    return await service.get_by_id(payment_method_id, user)


@router.get("", response_model=Page[PaymentMethodResponse])
async def list_by_user(
    service: Annotated[PaymentMethodService, Depends(get_payment_method_service)],
    user: Annotated[User, Depends(get_current_user)],
    params: Annotated[Params, Depends()],
    active: bool | None = None,
):

    return await service.list_by_user(user, active, params)
