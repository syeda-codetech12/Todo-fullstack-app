from sqlmodel import SQLModel
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @validator("name")
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        return v


class UserRegisterResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime
