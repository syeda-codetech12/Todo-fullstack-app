from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import get_current_user_id
from typing import Optional
from config import settings


security = HTTPBearer()


def get_current_user_id_from_token(request: Request) -> str:
    """
    Get the current user ID from the authorization token.
    This function is used as a dependency in protected routes.
    """
    # Check if middleware set an auth error
    if hasattr(request.state, 'auth_error') and request.state.auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=request.state.auth_error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # If no auth error, get user_id from state
    if hasattr(request.state, 'user_id') and request.state.user_id:
        return request.state.user_id
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_admin_access(user_id: str = Depends(get_current_user_id_from_token)):
    """
    Verify that the current user has admin access.
    This is a placeholder function - in a real application, 
    you would check if the user has an 'admin' role.
    """
    # In a real application, you would check user roles here
    # For now, we'll just return the user_id to indicate successful verification
    return user_id


def verify_user_access(target_user_id: str, current_user_id: str = Depends(get_current_user_id_from_token)):
    """
    Verify that the current user has access to the target user's resources.
    This is used to ensure users can only access their own data.
    """
    if current_user_id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )
    return current_user_id