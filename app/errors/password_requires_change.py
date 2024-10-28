from fastapi import status

class PasswordRequiresChange(Exception):
    def __init__(self, message: str = "Password requires change", status_code : int = status.HTTP_403_FORBIDDEN):
        self.message = message
        self.status_code = status_code