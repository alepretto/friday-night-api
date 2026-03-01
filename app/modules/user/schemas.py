from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    language: Optional[str] = None


class LinkTelegramRequest(BaseModel):
    init_data: str
