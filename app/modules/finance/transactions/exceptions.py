from http import HTTPStatus

from app.core.exception import FridayNightException


class TransactionNotFound(FridayNightException):
    def __init__(
        self,
        message: str = "Transaction Not Found",
        status_code: int = HTTPStatus.NOT_FOUND,
    ) -> None:
        super().__init__(message, status_code)


class TransactionAccessDenied(FridayNightException):
    def __init__(
        self,
        message: str = "Access Denied",
        status_code: int = HTTPStatus.FORBIDDEN,
    ) -> None:
        super().__init__(message, status_code)
