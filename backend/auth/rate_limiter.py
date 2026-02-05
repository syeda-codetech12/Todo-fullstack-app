from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException, status
from config import settings
import time


class RateLimiter:
    """
    Simple in-memory rate limiter that tracks requests per user.
    In a production environment, you would typically use Redis or similar for distributed rate limiting.
    """
    
    def __init__(self):
        # Dictionary to store request times for each user: {user_id: [request_times]}
        self.requests: Dict[str, list] = defaultdict(list)
        
    def is_allowed(self, user_id: str) -> bool:
        """
        Check if the user is allowed to make a request based on rate limits.
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=settings.rate_limit_window)
        
        # Clean up old requests outside the time window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id] 
            if req_time > window_start
        ]
        
        # Check if the user has exceeded the rate limit
        if len(self.requests[user_id]) >= settings.rate_limit_requests:
            return False
        
        # Add the current request time
        self.requests[user_id].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(user_id: str):
    """
    Check if the user has exceeded the rate limit.
    Raises an HTTPException if the rate limit is exceeded.
    """
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {settings.rate_limit_requests} requests per hour."
        )