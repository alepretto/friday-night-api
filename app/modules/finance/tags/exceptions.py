from http import HTTPStatus

from app.core.exception import FridayNightException


class TagAlreadyExists(FridayNightException):
    def __init__(
        self, message="Tag Already Exists", status_code: int = HTTPStatus.CONFLICT
    ) -> None:
        super().__init__(message, status_code)


class TagNotFound(FridayNightException):
    def __init__(
        self, message: str = "Tag Not Found!", status_code: int = HTTPStatus.BAD_REQUEST
    ) -> None:
        super().__init__(message, status_code)


class TagIntegrityError(FridayNightException):
    def __init__(
        self,
        message: str = "Category and Subcategory don't match",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ) -> None:
        super().__init__(message, status_code)
