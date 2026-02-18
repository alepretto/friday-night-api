import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel


class TransactionCreate(SQLModel):
    account_id: uuid.UUID
    transaction_tag_id: uuid.UUID
    payment_method_id: uuid.UUID
    currency_id: uuid.UUID

    value: Decimal
    description: Optional[str] = None
    date_transaction: Optional[datetime] = None


class TransactionResponse(TransactionCreate):
    id: uuid.UUID

    created_at: datetime
    updated_at: datetime
