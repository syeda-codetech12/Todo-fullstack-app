from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Union
import traceback
import logging
from config import settings


# Set up logging
logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
logger = logging.getLogger(__name__)


class TaskAPIException(HTTPException):
    """
    Base exception class for the Task API.
    """
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(TaskAPIException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: str):
        super().__init__(
            detail=f"User with ID {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class TaskNotFoundException(TaskAPIException):
    """
    Exception raised when a task is not found.
    """
    def __init__(self, task_id: str):
        super().__init__(
            detail=f"Task with ID {task_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class UnauthorizedAccessException(TaskAPIException):
    """
    Exception raised when a user tries to access resources they don't own.
    """
    def __init__(self):
        super().__init__(
            detail="Access denied: You can only access your own resources",
            status_code=status.HTTP_403_FORBIDDEN
        )


class DuplicateUserEmailException(TaskAPIException):
    """
    Exception raised when trying to create a user with an existing email.
    """
    def __init__(self, email: str):
        super().__init__(
            detail=f"User with email {email} already exists",
            status_code=status.HTTP_409_CONFLICT
        )


class InvalidCredentialsException(TaskAPIException):
    """
    Exception raised when invalid credentials are provided.
    """
    def __init__(self):
        super().__init__(
            detail="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ExpiredTokenException(TaskAPIException):
    """
    Exception raised when a token has expired.
    """
    def __init__(self):
        super().__init__(
            detail="Token has expired",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class RateLimitExceededException(TaskAPIException):
    """
    Exception raised when rate limit is exceeded.
    """
    def __init__(self, limit: int, window: int):
        super().__init__(
            detail=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )


async def global_exception_handler(request: Request, exc: Union[Exception, TaskAPIException]):
    """
    Global exception handler for the application.
    """
    if isinstance(exc, TaskAPIException):
        # Log the error
        logger.warning(f"TaskAPIException: {exc.detail} - Path: {request.url.path}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.detail,
                    "path": request.url.path,
                }
            }
        )
    else:
        # Log the full traceback for unexpected errors
        logger.error(f"Unexpected error: {str(exc)}\n{traceback.format_exc()}")
        
        # Return a generic error message to the client
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "path": request.url.path,
                }
            }
        )


def add_exception_handlers(app):
    """
    Add exception handlers to the FastAPI application.
    """
    app.add_exception_handler(TaskAPIException, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)