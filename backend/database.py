from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
from config import settings
import os

# Import models to ensure they are registered with SQLModel metadata
from models.user import User
from models.task import Task

# Use Neon database URL if available, otherwise use standard database URL
DATABASE_URL = settings.neon_database_url or settings.database_url

# Replace postgresql:// with postgresql+asyncpg:// to use async driver
if DATABASE_URL.startswith("postgresql://"):
    # Extract the connection parameters from the original URL
    base_url = DATABASE_URL.replace("postgresql://", "", 1)
    # Split credentials and host info
    if "@" in base_url:
        creds, host_part = base_url.split("@", 1)
        # For asyncpg, we need to remove query parameters like sslmode
        if "?" in host_part:
            host_info, params = host_part.split("?", 1)
        else:
            host_info = host_part
            params = ""
        
        # Reconstruct the URL for asyncpg
        DATABASE_URL = f"postgresql+asyncpg://{creds}@{host_info}"
    else:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,   # Verify connections before use
    pool_size=5,          # Number of connection pools
    max_overflow=10,      # Max overflow connections
    pool_recycle=300,     # Recycle connections after 5 minutes
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session.
    Used as a dependency in FastAPI routes.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_and_tables():
    """
    Create database tables.
    This function should be called during application startup.
    """
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)
