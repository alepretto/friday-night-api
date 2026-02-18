import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, Index, SQLModel, func
from uuid6 import uuid7


class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_methods"  # type: ignore
    __table_args__ = (Index("payment_method_idx", "user_id", "label", unique=True),)

    id: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid7)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, ondelete="CASCADE")

    label: str = Field(index=True)
    is_active: Optional[bool] = Field(default=True)

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
