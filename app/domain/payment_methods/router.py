from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.domain import get_payment_method_service
from app.domain.payment_methods.schemas import (
    PaymentMethodCreate,
    PaymentMethodResponse,
)
from app.domain.payment_methods.service import PaymentMethodService
from app.modules.user.model import User

router = APIRouter(prefix="/payment-methods", tags=["payment-methods"])


@router.post("", response_model=PaymentMethodResponse, status_code=HTTPStatus.CREATED)
async def create_payment_methods(
    payload: PaymentMethodCreate,
    service: Annotated[PaymentMethodService, Depends(get_payment_method_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)
