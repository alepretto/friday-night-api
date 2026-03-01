from app.core.exception import FridayNightException


class CardNotFound(FridayNightException):
    def __init__(self, status_code: int = 404) -> None:
        super().__init__("Card not found", status_code)
