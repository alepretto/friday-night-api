import uuid
from datetime import datetime

from sqlmodel import SQLModel
from pydantic import field_serializer

from app.core.utils import to_local


class TagCreate(SQLModel):
    category_id: uuid.UUID
    subcategory_id: uuid.UUID
    active: bool = True


class TagBase(TagCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def to_iso(self, dt):
        return to_local(dt)
