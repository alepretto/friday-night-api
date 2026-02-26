from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_holding_service
from app.modules.finance.holdings.schemas import HoldingCreate, HoldingResponse
from app.modules.finance.holdings.service import HoldingService
from app.modules.user.model import User

router = APIRouter(prefix="/holdings", tags=["holdings"])


@router.post("", response_model=HoldingResponse, status_code=HTTPStatus.CREATED)
async def create_holding(
    payload: HoldingCreate,
    service: Annotated[HoldingService, Depends(get_holding_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_update(payload, user)
