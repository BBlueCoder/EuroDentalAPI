from fastapi import status

class InvalidToken(Exception):
    def __init__(self, message: str = "Invalid token", status_code : int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code