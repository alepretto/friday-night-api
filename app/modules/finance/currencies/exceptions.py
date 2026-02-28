from http import HTTPStatus

from app.core.exception import FridayNightException


class CurrencyAlreadyExists(FridayNightException):
    def __init__(
        self, label: str, symbol: str, status_code: int = HTTPStatus.CONFLICT
    ) -> None:
        message = f"Currency already exists: {label} - {symbol}"
        super().__init__(message, status_code)


class CurrencyNotFound(FridayNightException):
    def __init__(self) -> None:
        super().__init__("Currency not found", HTTPStatus.NOT_FOUND)
