from sqlmodel import SQLModel as _SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class SQLModel(_SQLModel):
    """
    Base SQLModel class that adds common fields to all models.
    This extends the base SQLModel class to include common fields like id, timestamps, etc.
    """
    pass


def generate_uuid():
    """Generate a new UUID"""
    return str(uuid.uuid4())


class TimestampMixin:
    """
    Mixin class to add created_at and updated_at timestamp fields to models.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)


class UUIDPrimaryKey:
    """
    Mixin class to add a UUID primary key field to models.
    """
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True, nullable=False)