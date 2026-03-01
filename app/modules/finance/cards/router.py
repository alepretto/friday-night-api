import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from app.api.deps.core import get_current_user
from app.api.deps.finance import get_card_service
from app.modules.finance.cards.schemas import CardCreate, CardResponse
from app.modules.finance.cards.service import CardService
from app.modules.user.model import User

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("", response_model=CardResponse, status_code=HTTPStatus.CREATED)
async def create_card(
    payload: CardCreate,
    service: Annotated[CardService, Depends(get_card_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.create(payload, user)


@router.get("", response_model=Page[CardResponse])
async def list_cards_by_account(
    account_id: uuid.UUID,
    service: Annotated[CardService, Depends(get_card_service)],
    user: Annotated[User, Depends(get_current_user)],
    params: Annotated[Params, Depends()],
):
    return await service.list_by_account(account_id, user, params)


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: uuid.UUID,
    service: Annotated[CardService, Depends(get_card_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await service.get_by_id(card_id, user)


@router.delete("/{card_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_card(
    card_id: uuid.UUID,
    service: Annotated[CardService, Depends(get_card_service)],
    user: Annotated[User, Depends(get_current_user)],
):
    await service.delete(card_id, user)
