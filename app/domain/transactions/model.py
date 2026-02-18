import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import TIMESTAMP, Column
from sqlmodel import DECIMAL, Field, Relationship, SQLModel, func
from uuid6 import uuid7


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"  # type: ignore

    id: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid7)

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    account_id: uuid.UUID = Field(foreign_key="accounts.id", index=True)
    transaction_tag_id: uuid.UUID = Field(foreign_key="transaction_tags.id", index=True)
    payment_method_id: uuid.UUID = Field(foreign_key="payment_methods.id", index=True)
    currency_id: uuid.UUID = Field(foreign_key="currencies.id")

    value: Decimal = Field(DECIMAL(28, 6))

    date_transaction: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(TIMESTAMP(timezone=True)),
    )

    description: Optional[str] = Field(default=None, nullable=True)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now()),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )
