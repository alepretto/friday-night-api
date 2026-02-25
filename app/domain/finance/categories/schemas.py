import uuid
from datetime import datetime

from pydantic import field_serializer
from sqlmodel import SQLModel

from app.core.utils import to_local
from app.domain.finance.categories.model import CategoryType


class CategoryCreate(SQLModel):
    label: str
    type: CategoryType


class CategoryBase(CategoryCreate):
    id: uuid.UUID

    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def to_iso(self, dt):
        return to_local(dt)
