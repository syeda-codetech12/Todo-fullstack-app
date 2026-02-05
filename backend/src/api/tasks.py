from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from ..database import get_session
from ..models.user import User
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..auth.jwt_handler import get_current_user


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def get_tasks(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    '''
    Retrieve all tasks for the current user.
    '''
    # Only return tasks belonging to the current user
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return tasks


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    '''
    Create a new task for the current user.
    '''
    # Create task with the current user's ID
    db_task = Task()
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db_task.due_date = task.due_date
    db_task.user_id = current_user.id
    db_task.created_at = datetime.utcnow()
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    '''
    Retrieve a specific task by ID.
    '''
    # Get task and ensure it belongs to the current user
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    '''
    Update a specific task by ID.
    '''
    # Get task and ensure it belongs to the current user
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this task")
    
    # Update task with provided values
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    '''
    Delete a specific task by ID.
    '''
    # Get task and ensure it belongs to the current user
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this task")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
