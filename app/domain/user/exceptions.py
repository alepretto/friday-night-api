from app.core.exception import FridayNightException


class UserNotFoundError(FridayNightException):
    def __init__(self, message: str = "User not found", status_code: int = 404) -> None:
        super().__init__(message, status_code)
