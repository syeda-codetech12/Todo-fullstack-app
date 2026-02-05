import pytest
from fastapi.testclient import TestClient
from main import app
from models.user import User
from models.task import Task
from sqlmodel import Session, select
from auth.jwt_handler import create_access_token
from utils.helpers import generate_uuid


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def create_test_user_and_token(session: Session) -> tuple[User, str]:
    """Helper function to create a test user and return their token."""
    user = User(
        email="testuser@example.com",
        hashed_password="hashed_password_here",
        first_name="Test",
        last_name="User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create a token for the user
    token = create_access_token(data={"sub": user.id})
    return user, token


def test_create_task(client: TestClient, session: Session):
    """Test creating a new task."""
    user, token = create_test_user_and_token(session)
    
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }
    
    response = client.post(
        f"/api/users/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["priority"] == task_data["priority"]
    assert data["user_id"] == user.id


def test_get_user_tasks(client: TestClient, session: Session):
    """Test retrieving all tasks for a user."""
    user, token = create_test_user_and_token(session)
    
    # Create a task first
    task_data = {
        "title": "Get Tasks Test",
        "description": "This is a test task for getting tasks",
        "status": "pending",
        "priority": "high"
    }
    
    response = client.post(
        f"/api/users/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Now get the tasks
    response = client.get(
        f"/api/users/{user.id}/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) >= 1
    assert data["tasks"][0]["title"] == task_data["title"]


def test_get_specific_task(client: TestClient, session: Session):
    """Test retrieving a specific task."""
    user, token = create_test_user_and_token(session)
    
    # Create a task first
    task_data = {
        "title": "Specific Task",
        "description": "This is a specific test task",
        "status": "in_progress",
        "priority": "low"
    }
    
    response = client.post(
        f"/api/users/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_task = response.json()
    task_id = created_task["id"]
    
    # Now get the specific task
    response = client.get(
        f"/api/users/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_update_task(client: TestClient, session: Session):
    """Test updating a task."""
    user, token = create_test_user_and_token(session)
    
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "status": "pending",
        "priority": "medium"
    }
    
    response = client.post(
        f"/api/users/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_task = response.json()
    task_id = created_task["id"]
    
    # Now update the task
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "status": "completed"
    }
    
    response = client.put(
        f"/api/users/{user.id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]


def test_delete_task(client: TestClient, session: Session):
    """Test deleting a task."""
    user, token = create_test_user_and_token(session)
    
    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "status": "pending",
        "priority": "medium"
    }
    
    response = client.post(
        f"/api/users/{user.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    created_task = response.json()
    task_id = created_task["id"]
    
    # Now delete the task
    response = client.delete(
        f"/api/users/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    # Verify the task is soft deleted by trying to get it
    response = client.get(
        f"/api/users/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_user_data_isolation(client: TestClient, session: Session):
    """Test that users can only access their own tasks."""
    # Create two different users
    user1, token1 = create_test_user_and_token(session)
    
    # Create a second user
    user2 = User(
        email="testuser2@example.com",
        hashed_password="hashed_password_here",
        first_name="Test2",
        last_name="User2"
    )
    session.add(user2)
    session.commit()
    session.refresh(user2)
    
    # Create a token for user2
    token2 = create_access_token(data={"sub": user2.id})
    
    # User1 creates a task
    task_data = {
        "title": "User1's Task",
        "description": "This belongs to user1",
        "status": "pending",
        "priority": "medium"
    }
    
    response = client.post(
        f"/api/users/{user1.id}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    created_task = response.json()
    task_id = created_task["id"]
    
    # User2 should not be able to access User1's task
    response = client.get(
        f"/api/users/{user1.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403  # Forbidden