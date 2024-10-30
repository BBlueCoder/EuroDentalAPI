from fastapi import status

class LoginCredentialsInvalid(Exception):
    def __init__(self, message: str = "Email or Password are invalid", status_code : int = status.HTTP_403_FORBIDDEN):
        self.message = message
        self.status_code = status_code
