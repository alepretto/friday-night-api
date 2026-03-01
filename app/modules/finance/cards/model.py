import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import TIMESTAMP, Column, func
from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class CardFlag(str, Enum):
    mastercard = "mastercard"
    visa = "visa"


class Card(SQLModel, table=True):
    __tablename__ = "cards"  # type: ignore
    __table_args__ = {"schema": "finance"}

    id: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid7)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    account_id: uuid.UUID = Field(
        foreign_key="finance.accounts.id", index=True, ondelete="CASCADE"
    )

    label: str
    flag: CardFlag
    close_day: int
    due_day: int
    limit: float

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
