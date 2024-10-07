class LoginCredentialsInvalid(Exception):
    def __init__(self, message: str = "Email or Password are invalid"):
        self.message = message
