from datetime import datetime
from enum import Enum
import uuid
from uuid6 import uuid7

from sqlalchemy import Column, UniqueConstraint
from sqlmodel import SQLModel, Field, TIMESTAMP, func


class CategoryType(str, Enum):
    OUTCOME = "outcome"
    INCOME = "income"


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "label", "type", name="uq_finance_categories"),
        {"schema": "finance"},
    )

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")

    label: str = Field(index=True)
    type: CategoryType

    created_at: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
        ),
    )
