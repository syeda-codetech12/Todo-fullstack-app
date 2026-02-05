from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from models.user import UserPublic


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('first_name', 'last_name')
    def validate_name_length(cls, v):
        if v and len(v) > 50:
            raise ValueError('Name must be less than 50 characters')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('first_name', 'last_name')
    def validate_name_length(cls, v):
        if v and len(v) > 50:
            raise ValueError('Name must be less than 50 characters')
        return v


class UserResponse(UserPublic):
    """
    Schema for returning user information in API responses.
    Inherits from UserPublic to include only public fields.
    """
    pass


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data.
    """
    user_id: Optional[str] = None