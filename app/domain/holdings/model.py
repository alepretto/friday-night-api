import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlmodel import DECIMAL, TIMESTAMP, Field, SQLModel, func
from uuid6 import uuid7


class AssetType(str, Enum):
    CRIPTO = "cripto"
    STOCK = "stock"
    ETF = "etf"
    BOND = "bond"


class Holding(SQLModel, table=True):
    __tablename__ = "holdings"  # type: ignore
    __table_args__ = ({"schema": "finance"},)

    id: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid7)

    transaction_id: uuid.UUID = Field(foreign_key="transactions.id", index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")

    symbol: str = Field(index=True)
    asset_type: AssetType

    quantity: Decimal = Field(DECIMAL(28, 6))
    price: Decimal = Field(DECIMAL(28, 6))

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
