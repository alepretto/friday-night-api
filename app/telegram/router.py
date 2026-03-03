from typing import Optional

from fastapi import APIRouter, Header, HTTPException

from app.core.config import settings
from app.telegram.schema import TelegramUpdate
from app.telegram.service import telegram_bot_service

router = APIRouter(prefix="/telegram")


@router.post("/webhook")
async def telegram_webhook(
    update: TelegramUpdate,
    x_telegram_bot_api_secret_token: Optional[str] = Header(default=None),
):
    if (
        settings.TELEGRAM_WEBHOOK_SECRET
        and x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET
    ):
        raise HTTPException(status_code=403, detail="Invalid secret token")

    await telegram_bot_service.handle_update(update)
    return {"ok": True}
