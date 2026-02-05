"""
Main application module for the Secure Task API.

This module initializes the FastAPI application, configures middleware,
includes routers, and sets up lifespan events for database initialization.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import auth, tasks
from config import settings
from utils.helpers import utc_now
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.auth_middleware import AuthRateLimitMiddleware
from errors.handler import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    Runs startup and shutdown events.
    """
    # Startup: Create database tables
    await create_db_and_tables()
    print(f"[{utc_now()}] Database tables created successfully")

    yield  # Application runs here

    # Shutdown: Cleanup code would go here if needed
    print(f"[{utc_now()}] Application shutdown")


# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    description="A secure, user-specific RESTful API for managing tasks",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware
app.add_middleware(AuthRateLimitMiddleware)

# Add exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for the API.
    """
    return {
        "status": "healthy",
        "timestamp": utc_now(),
        "service": settings.app_name
    }