from fastapi import status

class InsufficientStock(Exception):
    def __init__(self, message = "Insufficient Stock to fulfill the request", status_code = status.HTTP_409_CONFLICT):
        self.message = message
        self.status_code = status_code