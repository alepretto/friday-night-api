import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.types import TIMESTAMP
from sqlmodel import Field, SQLModel, UniqueConstraint, func
from uuid6 import uuid7


class InstitutionType(str, Enum):
    BANK = "bank"
    FINTECH = "fintech"
    BROKER = "broker"
    EXCHANGE = "exchange"
    WALLET = "wallet"


class FinancialInstitution(SQLModel, table=True):
    __tablename__ = "financial_institutions"  # type: ignore

    __table_args__ = (
        UniqueConstraint("name", "type", name="uq_financial_institutions_name_type"),
    )
    id: uuid.UUID = Field(
        primary_key=True, index=True, nullable=False, default_factory=uuid7
    )

    name: str = Field(index=True)
    type: InstitutionType
    icon_url: Optional[str] = Field(default=None, nullable=True)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
        ),
    )
