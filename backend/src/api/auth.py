from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database import get_session
from ..models.user import User
from ..schemas.user import UserRegisterRequest, UserRegisterResponse
from ..auth.security import get_password_hash
from datetime import datetime
import uuid


def validate_email_format(email: str) -> bool:
    """Validate email format using regex"""
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> bool:
    """Validate password strength requirements"""
    # At least 8 characters, one uppercase, one lowercase, one digit
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit


router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
def register_user(user_data: UserRegisterRequest, session: Session = Depends(get_session)):
    # Validate email format
    if not validate_email_format(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Validate password strength
    if not validate_password_strength(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters with uppercase, lowercase, and digit"
        )
    
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Return response
    return UserRegisterResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.post("/login")
def login_user():
    # This is a simplified version - will be expanded later
    return {"message": "Login endpoint"}


@router.post("/refresh")
def refresh_token():
    # This would normally take a refresh token and generate a new access token
    # For now, we'll just return a new access token for demonstration
    return {"message": "Token refresh endpoint"}
