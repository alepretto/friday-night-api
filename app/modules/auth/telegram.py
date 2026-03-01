import hashlib
import hmac
import json
import time
import urllib.parse

from app.modules.auth.exceptions import TelegramAuthError


def validate_init_data(init_data: str, bot_token: str) -> dict:
    parsed = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise TelegramAuthError("hash ausente")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    computed = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed, received_hash):
        raise TelegramAuthError("hash inválido")

    if time.time() - int(parsed.get("auth_date", 0)) > 300:
        raise TelegramAuthError("initData expirado")

    return parsed


def extract_telegram_id(parsed: dict) -> int:
    user_json = parsed.get("user")
    if not user_json:
        raise TelegramAuthError("campo user ausente no initData")
    user_data = json.loads(user_json)
    telegram_id = user_data.get("id")
    if not telegram_id:
        raise TelegramAuthError("id ausente no user do initData")
    return int(telegram_id)
