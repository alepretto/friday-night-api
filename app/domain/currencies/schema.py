import uuid
from datetime import datetime

from sqlmodel import SQLModel

from app.domain.currencies.model import CurrencyType


class CurrencyCreate(SQLModel):
    label: str
    symbol: str
    type: CurrencyType


class CurrencyResponse(CurrencyCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
