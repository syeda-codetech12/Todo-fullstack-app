from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum
import uuid
from models.base import UUIDPrimaryKey, TimestampMixin
from sqlalchemy import Index

if TYPE_CHECKING:
    from models.user import User


class TaskStatus(str, Enum):
    """
    Enum for task status values.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """
    Enum for task priority values.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    user_id: str = Field(foreign_key="user.id", nullable=False)  # Links to User model
    completed_at: Optional[datetime] = Field(default=None, nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)  # For soft deletion


class Task(TaskBase, UUIDPrimaryKey, TimestampMixin, table=True):
    """
    Task model representing a user's task with properties like title, description, status, etc.
    """
    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    # Indexes
    __table_args__ = (
        # Index on user_id for efficient retrieval of user-specific tasks
        Index('ix_tasks_user_id', 'user_id'),
        # Index on status for filtering tasks by status
        Index('ix_tasks_status', 'status'),
        # Index on due_date for sorting and filtering by deadline
        Index('ix_tasks_due_date', 'due_date'),
        # Index on deleted_at for excluding soft-deleted records
        Index('ix_tasks_deleted_at', 'deleted_at'),
        # Composite index on (user_id, status) for efficient queries of user tasks by status
        Index('ix_tasks_user_id_status', 'user_id', 'status'),
        {'sqlite_autoincrement': True},
    )


class TaskPublic(TaskBase):
    """
    Public representation of Task model (without sensitive data).
    """
    id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    deleted_at: Optional[datetime]


# Add relationship to User model (this needs to be done after Task is defined)
# This is handled by the Relationship field in Task model