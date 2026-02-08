from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from datetime import timedelta
from auth.jwt_handler import create_access_token, create_refresh_token, get_password_hash, verify_password, verify_access_token
from auth.security import get_current_user_id_from_token
from database import get_async_session
from models.user import User, UserPublic
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from utils.helpers import validate_email
import uuid


# Define UserLogin here if not imported properly
try:
    UserLogin
except NameError:
    from pydantic import BaseModel

    class UserLogin(BaseModel):
        email: str
        password: str


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Register a new user.
    """
    # Validate email format
    if not validate_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Check if user already exists
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin, session: AsyncSession = Depends(get_async_session)):
    """
    Authenticate user and return JWT tokens.
    """
    # Find user by email
    result = await session.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=30)  # This can be configurable
    refresh_token_expires = timedelta(days=7)  # This can be configurable
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": user.id},
        expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(request: Request, session: AsyncSession = Depends(get_async_session)):
    """
    Refresh access token using refresh token.
    """
    try:
        # Get refresh token from request body
        body = await request.json()
        refresh_token = body.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required",
            )
        
        payload = verify_access_token(refresh_token)
        
        # Check if token type is refresh
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Verify user still exists and is active
        user = await session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=30)  # This can be configurable
        new_access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        # Create new refresh token
        refresh_token_expires = timedelta(days=7)  # This can be configurable
        new_refresh_token = create_refresh_token(
            data={"sub": user.id},
            expires_delta=refresh_token_expires
        )
        
        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user_id: str = Depends(get_current_user_id_from_token),
                         session: AsyncSession = Depends(get_async_session)):
    """
    Get current user information.
    """
    user = await session.get(User, current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user