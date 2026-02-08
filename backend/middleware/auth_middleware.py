from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt_handler import verify_access_token
from auth.rate_limiter import check_rate_limit
import time


class AuthRateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle authentication and rate limiting.
    """

    async def dispatch(self, request: Request, call_next):
        # Extract the path and method
        path = request.url.path
        method = request.method

        # Skip authentication and rate limiting for certain paths
        if path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
            response = await call_next(request)
            return response

        # Skip authentication for OPTIONS requests (preflight requests)
        if method == "OPTIONS":
            response = await call_next(request)
            return response

        # Skip authentication for public auth endpoints (register, login, refresh)
        if path.startswith("/api/auth/") and any(endpoint in path for endpoint in ["/register", "/login", "/refresh"]):
            # Still apply rate limiting for these endpoints to prevent abuse
            # For now, we'll skip rate limiting for these endpoints
            response = await call_next(request)
            return response
        elif path.startswith("/api/auth"): 
            # For other auth endpoints (like /me), require authentication
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                # Set a flag in request state to indicate authentication failure
                request.state.auth_error = "Not authenticated"
            else:
                token = auth_header.split(" ")[1]
                try:
                    payload = verify_access_token(token)
                    user_id = payload.get("sub")

                    if not user_id:
                        # Set a flag in request state to indicate authentication failure
                        request.state.auth_error = "Could not validate credentials"
                    else:
                        # Add user_id to request state for use in endpoints
                        request.state.user_id = user_id

                        # Check rate limit for authenticated user
                        check_rate_limit(user_id)

                except Exception:
                    # Set a flag in request state to indicate authentication failure
                    request.state.auth_error = "Could not validate credentials"
        else:
            # For non-auth endpoints, require authentication
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                # Set a flag in request state to indicate authentication failure
                request.state.auth_error = "Not authenticated"
            else:
                token = auth_header.split(" ")[1]
                try:
                    payload = verify_access_token(token)
                    user_id = payload.get("sub")

                    if not user_id:
                        # Set a flag in request state to indicate authentication failure
                        request.state.auth_error = "Could not validate credentials"
                    else:
                        # Add user_id to request state for use in endpoints
                        request.state.user_id = user_id

                        # Check rate limit for authenticated user
                        check_rate_limit(user_id)

                except Exception:
                    # Set a flag in request state to indicate authentication failure
                    request.state.auth_error = "Could not validate credentials"

        response = await call_next(request)
        return response
