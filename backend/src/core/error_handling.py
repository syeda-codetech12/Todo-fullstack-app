from fastapi import HTTPException, status
from typing import Union
from ..models.user import UserRead
from ..models.task import TaskRead


class ErrorResponse:
    def __init__(self, detail: str):
        self.detail = detail


def create_response(data: Union[UserRead, TaskRead, list, dict, None], message: str = "Success"):
    return {
        "message": message,
        "data": data
    }


def handle_error(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    raise HTTPException(status_code=status_code, detail=detail)
