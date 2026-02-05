"""
User model module for the Secure Task API.

This module defines the User data model with all required fields,
validation rules, and relationships as specified in the data model.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import validator
import uuid
from models.base import UUIDPrimaryKey, TimestampMixin
from sqlalchemy import Index

if TYPE_CHECKING:
    from models.task import Task


class UserBase(SQLModel):
    """
    Base class for User model with common fields.

    Defines the common fields that are shared between the User model
    and any related schema classes.
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    is_active: bool = Field(default=True)


class User(UserBase, UUIDPrimaryKey, TimestampMixin, table=True):
    """
    User model representing an authenticated user of the system.
    """
    # Password is stored as a hash
    hashed_password: str = Field(nullable=False)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    # Indexes
    __table_args__ = (
        # Index on email for fast lookup during authentication
        Index('ix_users_email', 'email'),
        # Index on is_active for filtering active users
        Index('ix_users_is_active', 'is_active'),
        {'sqlite_autoincrement': True},
    )

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v

    @validator('first_name', 'last_name')
    def validate_name_length(cls, v):
        if v and len(v) > 50:
            raise ValueError('Name must be less than 50 characters')
        return v


class UserPublic(UserBase):
    """
    Public representation of User model (without sensitive data).
    """
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool