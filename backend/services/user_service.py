from sqlmodel import Session, select
from typing import Optional
from models.user import User
from schemas.user import UserCreate
from auth.jwt_handler import get_password_hash
from utils.helpers import validate_email


class UserService:
    """
    Service class for handling user-related operations.
    """
    
    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """
        Create a new user.
        """
        # Validate email format
        if not validate_email(user_create.email):
            raise ValueError("Invalid email format")
        
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_create.email)
        ).first()
        
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        db_user = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            first_name=user_create.first_name,
            last_name=user_create.last_name
        )
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        user = session.exec(select(User).where(User.email == email)).first()
        return user
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by ID.
        """
        user = session.get(User, user_id)
        return user
    
    @staticmethod
    def update_user(session: Session, user_id: str, first_name: Optional[str] = None, 
                   last_name: Optional[str] = None) -> Optional[User]:
        """
        Update user information.
        """
        user = session.get(User, user_id)
        
        if not user:
            return None
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
            
        user.updated_at = session.exec(select(User).where(User.id == user_id)).first().updated_at
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user
    
    @staticmethod
    def deactivate_user(session: Session, user_id: str) -> bool:
        """
        Deactivate a user account.
        """
        user = session.get(User, user_id)
        
        if not user:
            return False
        
        user.is_active = False
        session.add(user)
        session.commit()
        
        return True