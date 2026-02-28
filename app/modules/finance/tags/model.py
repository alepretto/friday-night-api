from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid6 import uuid7
import uuid
from sqlmodel import Field, SQLModel, TIMESTAMP, func, Relationship
from sqlalchemy import Column, UniqueConstraint

if TYPE_CHECKING:
    from app.modules.finance.categories.model import Category
    from app.modules.finance.subcategories.model import Subcategory


class Tag(SQLModel, table=True):
    __tablename__ = "tags"  # type: ignore
    __table_args__ = (
        UniqueConstraint(
            "user_id", "category_id", "subcategory_id", name="uq_finance_tag"
        ),
        {"schema": "finance"},
    )

    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True, index=True)

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")
    category_id: uuid.UUID = Field(
        foreign_key="finance.categories.id", ondelete="CASCADE"
    )
    subcategory_id: uuid.UUID = Field(
        foreign_key="finance.subcategories.id", ondelete="CASCADE"
    )

    active: bool = Field(default=False)

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

    category: Optional["Category"] = Relationship()
    subcategory: Optional["Subcategory"] = Relationship()
