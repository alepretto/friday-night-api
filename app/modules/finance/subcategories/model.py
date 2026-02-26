import uuid
from datetime import datetime

from sqlalchemy import Column, UniqueConstraint
from sqlmodel import Field, SQLModel, TIMESTAMP, func
from uuid6 import uuid7


class Subcategory(SQLModel, table=True):
    __tablename__ = "subcategories"  # type: ignore
    __table_args__ = (
        UniqueConstraint("category_id", "label", name="uq_finance_subcategory"),
        {"schema": "finance"},
    )

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    category_id: uuid.UUID = Field(foreign_key="finance.categories.id", index=True)

    label: str = Field(index=True)

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
