from datetime import datetime
import uuid

from pydantic import field_serializer
from sqlmodel import SQLModel

from app.core.utils import to_local


class SubcategoryCreate(SQLModel):
    category_id: uuid.UUID
    label: str


class SubcategoryBase(SubcategoryCreate):
    id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def to_iso(self, dt):
        return to_local(dt)
