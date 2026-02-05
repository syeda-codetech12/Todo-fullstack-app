from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserLoginResponse(TokenResponse):
    id: str
    email: EmailStr
    name: str
