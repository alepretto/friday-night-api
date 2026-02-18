import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import field_serializer
from sqlmodel import SQLModel

from app.core.utils import to_local
from app.domain.holdings.model import AssetType


class HoldingCreate(SQLModel):
    transaction_id: uuid.UUID
    user_id: uuid.UUID
    symbol: str
    asset_type: AssetType
    quantity: Decimal
    price: Decimal


class HoldingResponse(HoldingCreate):
    id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def get_timezone(self, dt):
        return to_local(dt)
