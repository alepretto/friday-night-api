import uuid
from datetime import datetime

from sqlmodel import SQLModel
from pydantic import field_serializer

from app.core.utils import to_local
from app.modules.finance.categories.model import CategoryType


class TagCreate(SQLModel):
    category_id: uuid.UUID
    subcategory_id: uuid.UUID
    active: bool = True


class TagUpdate(SQLModel):
    category_id: uuid.UUID
    subcategory_id: uuid.UUID


class CategoryInTag(SQLModel):
    id: uuid.UUID
    label: str
    type: CategoryType


class SubcategoryInTag(SQLModel):
    id: uuid.UUID
    label: str


class TagBase(TagCreate):
    id: uuid.UUID
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def to_iso(self, dt):
        return to_local(dt)


class TagResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    category_id: uuid.UUID
    subcategory_id: uuid.UUID
    active: bool

    category: CategoryInTag
    subcategory: SubcategoryInTag

    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def to_iso(self, dt):
        return to_local(dt)
