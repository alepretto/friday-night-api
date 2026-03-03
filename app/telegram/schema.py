from typing import Optional

from pydantic import BaseModel, Field


class TelegramUser(BaseModel):
    id: int
    first_name: str
    username: Optional[str] = None


class TelegramChat(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    from_user: Optional[TelegramUser] = Field(default=None, alias="from")
    chat: TelegramChat
    text: Optional[str] = None

    model_config = {"populate_by_name": True}


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
