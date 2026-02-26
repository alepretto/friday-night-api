from http import HTTPStatus

from app.core.exception import FridayNightException


class TagAlreadyExists(FridayNightException):
    def __init__(
        self, message="Tag Already Exists", status_code: int = HTTPStatus.CONFLICT
    ) -> None:
        super().__init__(message, status_code)
