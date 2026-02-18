import uuid
from datetime import datetime

from sqlmodel import SQLModel


class PaymentMethodCreate(SQLModel):
    label: str
    is_active: bool = True


class PaymentMethodResposne(PaymentMethodCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime
