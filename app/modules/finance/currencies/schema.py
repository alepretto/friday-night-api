import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from app.modules.finance.currencies.model import CurrencyType


class CurrencyCreate(SQLModel):
    label: str
    symbol: str
    type: CurrencyType


class CurrencyUpdate(SQLModel):
    label: Optional[str] = None
    symbol: Optional[str] = None
    type: Optional[CurrencyType] = None


class CurrencyResponse(CurrencyCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
