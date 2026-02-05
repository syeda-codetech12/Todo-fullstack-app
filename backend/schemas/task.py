from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from models.task import TaskPublic, TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator('title')
    def validate_title_length(cls, v):
        if not v or len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @field_validator('description')
    def validate_description_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must not exceed 1000 characters')
        return v

    @field_validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

    @field_validator('title')
    def validate_title_length(cls, v):
        if v and (len(v) < 1 or len(v) > 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @field_validator('description')
    def validate_description_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must not exceed 1000 characters')
        return v

    @field_validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v


class TaskFilter(BaseModel):
    """
    Schema for filtering tasks.
    """
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    limit: int = 20
    offset: int = 0

    @field_validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Limit must be between 1 and 100')
        return v


class TaskResponse(TaskPublic):
    """
    Schema for returning task information in API responses.
    Inherits from TaskPublic to include only public fields.
    """
    pass


class TaskListResponse(BaseModel):
    """
    Schema for returning a list of tasks with pagination info.
    """
    tasks: list[TaskResponse]
    total_count: int