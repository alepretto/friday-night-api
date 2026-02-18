from http import HTTPStatus


class FridayNightException(Exception):
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST) -> None:

        self.message = message
        self.status_code = status_code
