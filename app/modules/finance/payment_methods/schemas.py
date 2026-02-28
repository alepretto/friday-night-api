import uuid
from datetime import datetime

from sqlmodel import SQLModel


class PaymentMethodCreate(SQLModel):
    label: str
    active: bool = True


class PaymentMethodResponse(PaymentMethodCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime
