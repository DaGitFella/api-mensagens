from fastapi import HTTPException, status
from http import HTTPStatus

class NotFoundException(HTTPException):
    def __init__(self, message: str = 'Resource not found'):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)