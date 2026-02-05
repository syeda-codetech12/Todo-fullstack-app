from fastapi import FastAPI
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .config import settings
from sqlmodel import SQLModel
from .database import engine, create_db_and_tables


def create_app():
    app = FastAPI(title="Todo App API", version="1.0.0")

    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])

    # Create tables
    @app.on_event("startup")
    def on_startup():
        SQLModel.metadata.create_all(bind=engine)
        create_db_and_tables()

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo App API"}

    return app


app = create_app()
