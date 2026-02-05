from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from models.task import Task, TaskStatus
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskFilter
from auth.rate_limiter import check_rate_limit


class TaskService:
    """
    Service class for handling task-related operations.
    """
    
    @staticmethod
    def create_task(session: Session, user_id: str, task_create: TaskCreate) -> Task:
        """
        Create a new task for a user.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        # Create task
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status,
            priority=task_create.priority,
            due_date=task_create.due_date,
            user_id=user_id
        )
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        return db_task
    
    @staticmethod
    def get_tasks_for_user(
        session: Session, 
        user_id: str, 
        filters: Optional[TaskFilter] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional filtering.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        # Build query with filters
        query = select(Task).where(Task.user_id == user_id, Task.deleted_at.is_(None))
        
        if filters:
            if filters.status:
                query = query.where(Task.status == filters.status)
            
            if filters.priority:
                query = query.where(Task.priority == filters.priority)
        
        # Apply pagination
        if filters:
            query = query.offset(filters.offset).limit(filters.limit)
        
        tasks = session.exec(query).all()
        return tasks
    
    @staticmethod
    def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a user.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        # Get task
        task = session.get(Task, task_id)
        
        if not task:
            return None
        
        # Verify that the task belongs to the specified user
        if task.user_id != user_id:
            return None
        
        # Verify that the task is not soft-deleted
        if task.deleted_at is not None:
            return None
        
        return task
    
    @staticmethod
    def update_task(
        session: Session, 
        task_id: str, 
        user_id: str, 
        task_update: TaskUpdate
    ) -> Optional[Task]:
        """
        Update an existing task for a user.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        # Get task
        db_task = session.get(Task, task_id)
        
        if not db_task:
            return None
        
        # Verify that the task belongs to the specified user
        if db_task.user_id != user_id:
            return None
        
        # Verify that the task is not soft-deleted
        if db_task.deleted_at is not None:
            return None
        
        # Update task fields
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)
        
        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()
        
        # Handle status change to completed
        if task_update.status == TaskStatus.COMPLETED and db_task.status != TaskStatus.COMPLETED:
            db_task.completed_at = datetime.utcnow()
        elif task_update.status != TaskStatus.COMPLETED and db_task.status == TaskStatus.COMPLETED:
            db_task.completed_at = None
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        return db_task
    
    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Soft delete a task for a user.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        # Get task
        db_task = session.get(Task, task_id)
        
        if not db_task:
            return False
        
        # Verify that the task belongs to the specified user
        if db_task.user_id != user_id:
            return False
        
        # Verify that the task is not already soft-deleted
        if db_task.deleted_at is not None:
            return False
        
        # Perform soft delete
        db_task.deleted_at = datetime.utcnow()
        db_task.updated_at = datetime.utcnow()
        
        session.add(db_task)
        session.commit()
        
        return True
    
    @staticmethod
    def get_task_count_for_user(session: Session, user_id: str, status: Optional[TaskStatus] = None) -> int:
        """
        Get the count of tasks for a user, optionally filtered by status.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        query = select(Task).where(Task.user_id == user_id, Task.deleted_at.is_(None))
        
        if status:
            query = query.where(Task.status == status)
        
        tasks = session.exec(query).all()
        return len(tasks)
    
    @staticmethod
    def get_overdue_tasks_for_user(session: Session, user_id: str) -> List[Task]:
        """
        Get all overdue tasks for a user.
        """
        # Check rate limit
        check_rate_limit(user_id)
        
        query = select(Task).where(
            Task.user_id == user_id,
            Task.due_date < datetime.utcnow(),
            Task.status != TaskStatus.COMPLETED,
            Task.deleted_at.is_(None)
        )
        
        tasks = session.exec(query).all()
        return tasks