from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from typing import List
from auth.security import get_current_user_id_from_token, verify_user_access
from auth.rate_limiter import check_rate_limit
from database import get_async_session
from models.task import Task, TaskPublic
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskFilter, TaskResponse, TaskListResponse
from datetime import datetime
import uuid


router = APIRouter(prefix="/users/{user_id}/tasks", tags=["Tasks"])


@router.get("/", response_model=TaskListResponse)
async def get_user_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id_from_token),
    filters: TaskFilter = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific user with optional filtering.
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user_id)

    # Check rate limit
    check_rate_limit(current_user_id)

    # Build query with filters
    query = select(Task).where(Task.user_id == user_id, Task.deleted_at.is_(None))

    if filters.status:
        query = query.where(Task.status == filters.status)

    if filters.priority:
        query = query.where(Task.priority == filters.priority)

    # Count total for pagination
    count_result = await session.execute(select(func.count()).select_from(query.subquery()))
    total_count = count_result.scalar()

    # Apply pagination
    query = query.offset(filters.offset).limit(filters.limit)

    result = await session.execute(query)
    tasks = result.scalars().all()

    return TaskListResponse(tasks=tasks, total_count=total_count)


@router.post("/", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user_id_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the specified user.
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user_id)

    # Check rate limit
    check_rate_limit(current_user_id)

    # Create task
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user_id
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for the specified user.
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user_id)

    # Check rate limit
    check_rate_limit(current_user_id)

    # Get task
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the specified user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to the specified user"
        )

    # Verify that the task is not soft-deleted
    if task.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing task for the specified user.
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user_id)

    # Check rate limit
    check_rate_limit(current_user_id)

    # Get task
    db_task = await session.get(Task, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the specified user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to the specified user"
        )

    # Verify that the task is not soft-deleted
    if db_task.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    # Handle status change to completed
    if task_update.status == "completed" and db_task.status != "completed":
        db_task.completed_at = datetime.utcnow()
    elif task_update.status != "completed" and db_task.status == "completed":
        db_task.completed_at = None

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.delete("/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user_id_from_token),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Soft delete an existing task for the specified user.
    """
    # Verify user has access to this resource
    verify_user_access(user_id, current_user_id)

    # Check rate limit
    check_rate_limit(current_user_id)

    # Get task
    db_task = await session.get(Task, task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the specified user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to the specified user"
        )

    # Verify that the task is not already soft-deleted
    if db_task.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Perform soft delete
    db_task.deleted_at = datetime.utcnow()
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    await session.commit()

    return {"message": "Task soft deleted successfully"}