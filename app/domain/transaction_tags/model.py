import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlmodel import TIMESTAMP, Field, Index, SQLModel, func
from uuid6 import uuid7


class TransactionTagType(str, Enum):
    OUTCOME = "outcome"
    INCOME = "income"


class TransactionTag(SQLModel, table=True):
    __tablename__ = "transaction_tags"  # type: ignore
    __table_args__ = (
        Index(
            "transaction_tag_idx",
            "user_id",
            "category",
            "subcategory",
            "type",
            unique=True,
        ),
    )

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

    category: str = Field(index=True)
    subcategory: str = Field(index=True)
    type: TransactionTagType

    is_active: bool = Field(default=True)

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
