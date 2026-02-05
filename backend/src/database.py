from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
import os
from .config import settings


# Enable WAL mode for SQLite to allow concurrent reads
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


# Create engine with appropriate settings
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args=connect_args
)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    # Import models to register them with SQLModel
    from .models.user import User
    from .models.task import Task
    from sqlmodel import SQLModel
    
    # Create tables
    SQLModel.metadata.create_all(engine)
