import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PendingTransaction(BaseModel):
    account_id: uuid.UUID
    tag_id: uuid.UUID
    payment_method_id: uuid.UUID
    currency_id: uuid.UUID
    value: Decimal
    description: Optional[str] = None
    date: Optional[datetime] = None

    # Labels for confirmation message
    account_label: str
    tag_label: str
    payment_method_label: str
    currency_symbol: str
