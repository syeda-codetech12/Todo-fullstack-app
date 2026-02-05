from datetime import datetime
from typing import Optional
import uuid
import re


def generate_uuid() -> str:
    """
    Generate a new UUID string.
    """
    return str(uuid.uuid4())


def validate_email(email: str) -> bool:
    """
    Validate an email address using a basic regex pattern.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string by removing potentially dangerous characters.
    This is a basic implementation - in production, use a more comprehensive sanitizer.
    """
    if input_str is None:
        return None
    
    # Remove potentially dangerous characters
    sanitized = input_str.replace('<', '').replace('>', '').replace('"', '').replace("'", "")
    return sanitized.strip()


def utc_now() -> datetime:
    """
    Get the current UTC time.
    """
    return datetime.utcnow()


def is_valid_datetime(dt_str: str) -> bool:
    """
    Check if a string is a valid datetime in ISO format.
    """
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def mask_sensitive_data(data: str, show_chars: int = 2) -> str:
    """
    Mask sensitive data like passwords or tokens, showing only the first few characters.
    """
    if not data or len(data) <= show_chars:
        return data
    
    return data[:show_chars] + '*' * (len(data) - show_chars)