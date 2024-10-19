from fastapi import status

class ItemNotFound(Exception):
    def __init__(self, message = "Item Not Found", status_code = status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code