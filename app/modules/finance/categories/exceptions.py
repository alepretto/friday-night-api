from http import HTTPStatus

from app.core.exception import FridayNightException


class CategoryAlreadyExistis(FridayNightException):
    def __init__(self, label: str, status_code=HTTPStatus.CONFLICT):

        message = f"This Category '{label}' already exists"

        super().__init__(message=message, status_code=status_code)
