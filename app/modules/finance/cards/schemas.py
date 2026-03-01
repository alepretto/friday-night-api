import uuid
from datetime import datetime

from sqlmodel import SQLModel

from .model import CardFlag


class CardCreate(SQLModel):
    account_id: uuid.UUID
    label: str
    flag: CardFlag
    close_day: int
    due_day: int
    limit: float


class CardResponse(CardCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
