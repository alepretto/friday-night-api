import uuid

from sqlmodel import SQLModel
from supabase_auth import datetime

from app.domain.currencies.model import CurrencyType


class CurrencyCreate(SQLModel):
    label: str
    symbol: str
    type: CurrencyType


class CurrencyResponse(CurrencyCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
