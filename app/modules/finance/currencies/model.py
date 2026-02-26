import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlmodel import TIMESTAMP, Field, Index, SQLModel, func
from uuid6 import uuid7


class CurrencyType(str, Enum):
    FIAT = "fiat"
    CRIPTO = "cripto"


class Currency(SQLModel, table=True):
    __tablename__ = "currencies"  # type: ignore

    __table_args__ = (
        Index("unique_currency_label_symbol", "label", "symbol", unique=True),
        {"schema": "finance"},
    )

    id: uuid.UUID = Field(
        primary_key=True, index=True, nullable=False, default_factory=uuid7
    )
    label: str = Field(index=True)
    symbol: str = Field(index=True)
    type: CurrencyType

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now()),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
