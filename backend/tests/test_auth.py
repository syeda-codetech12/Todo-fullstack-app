import pytest
from fastapi.testclient import TestClient
from main import app
from models.user import User
from sqlmodel import Session, select
from auth.jwt_handler import get_password_hash
from utils.helpers import generate_uuid


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_register_user(client: TestClient, session: Session):
    """Test user registration endpoint."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not return sensitive data


def test_register_user_duplicate_email(client: TestClient, session: Session):
    """Test registering a user with an existing email."""
    # First registration should succeed
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Second registration with same email should fail
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 409  # Conflict


def test_login_user_success(client: TestClient, session: Session):
    """Test successful user login."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Then try to log in
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(client: TestClient, session: Session):
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401  # Unauthorized


def test_get_current_user(client: TestClient, session: Session):
    """Test getting current user info."""
    # Register a user
    user_data = {
        "email": "current@example.com",
        "password": "testpassword123",
        "first_name": "Current",
        "last_name": "User"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Log in to get token
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    token_data = response.json()
    access_token = token_data["access_token"]
    
    # Get current user info
    response = client.get("/api/auth/me", 
                         headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    
    user_info = response.json()
    assert user_info["email"] == user_data["email"]
    assert user_info["first_name"] == user_data["first_name"]
    assert user_info["last_name"] == user_data["last_name"]