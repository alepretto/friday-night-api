import httpx

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.modules.user.repo import UserRepo
from app.agent.service import agent_service
from app.telegram.schema import TelegramUpdate


class TelegramBotService:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient()

    async def handle_update(self, update: TelegramUpdate) -> None:
        if not update.message:
            return

        msg = update.message
        chat_id = msg.chat.id
        text = msg.text

        if not text:
            return

        telegram_user_id = msg.from_user.id if msg.from_user else None
        if not telegram_user_id:
            return

        async with AsyncSessionLocal() as db:
            user = await UserRepo(db).get_by_telegram_id(telegram_user_id)
            if not user:
                await self.send_message(
                    chat_id,
                    "Sua conta Telegram não está vinculada. Acesse o app Friday Night para vincular.",
                )
                return

            reply = await agent_service.chat(chat_id, text, user, db)

        await self.send_message(chat_id, reply)

    async def send_message(self, chat_id: int, text: str) -> None:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            await self._client.post(url, json={"chat_id": chat_id, "text": text})
        except Exception:
            pass


telegram_bot_service = TelegramBotService()
