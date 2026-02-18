import uuid
from datetime import datetime

from sqlmodel import SQLModel

from app.domain.transaction_tags.model import TransactionTagType


class TransactionTagCreate(SQLModel):
    category: str
    subcategory: str
    type: TransactionTagType
    is_active: bool = True


class TransactionTagResponse(TransactionTagCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime
