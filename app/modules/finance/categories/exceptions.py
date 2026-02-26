from http import HTTPStatus

from app.core.exception import FridayNightException


class CategoryAlreadyExistis(FridayNightException):
    def __init__(self, label: str, status_code=HTTPStatus.CONFLICT):

        message = f"This Category '{label}' already exists"

        super().__init__(message=message, status_code=status_code)


class CategoryNotFound(FridayNightException):
    def __init__(
        self, message="category not found!", status_code: int = HTTPStatus.NOT_FOUND
    ) -> None:
        super().__init__(message, status_code)
