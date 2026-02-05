# Quickstart Guide: Secure Task API with User-Specific Data

## Overview
This guide provides instructions for setting up and running the Secure Task API locally. The API provides secure, user-specific CRUD operations for managing tasks using FastAPI, SQLModel, and Neon PostgreSQL.

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Access to Neon PostgreSQL (or local PostgreSQL for development)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi sqlmodel pyjwt python-multipart uvicorn pytest python-dotenv bcrypt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/task_api_dev
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours in minutes
NEON_DATABASE_URL=your-neon-database-url  # For production
```

### 5. Initialize the Database
```bash
# Run the database initialization script
python -c "
from backend.database import engine
from backend.models.user import User
from backend.models.task import Task
from sqlmodel import SQLModel

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

import asyncio
asyncio.run(create_db_and_tables())
"
```

## Running the Application

### Development Mode
```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### Production Mode
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/users/me` - Get current user info

### Task Management
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Soft delete a task

## Testing

### Run Unit Tests
```bash
pytest backend/tests/
```

### Run Specific Test Files
```bash
pytest backend/tests/test_auth.py
pytest backend/tests/test_tasks.py
```

## Key Components

### Models (`backend/models/`)
- `user.py` - User data model
- `task.py` - Task data model

### Schemas (`backend/schemas/`)
- `user.py` - User Pydantic schemas
- `task.py` - Task Pydantic schemas

### Routers (`backend/routers/`)
- `auth.py` - Authentication endpoints
- `tasks.py` - Task CRUD endpoints

### Authentication (`backend/auth/`)
- `jwt_handler.py` - JWT token creation and verification
- `security.py` - Authentication utilities
- `rate_limiter.py` - Rate limiting implementation

## Security Features

1. **JWT Token Authentication**: All protected routes require a valid JWT token
2. **User-Specific Data Isolation**: Users can only access their own tasks
3. **Password Hashing**: User passwords are securely hashed using bcrypt
4. **Input Validation**: All API inputs are validated using Pydantic schemas
5. **Rate Limiting**: API enforces 100 requests per hour per authenticated user
6. **Soft Deletion**: Tasks are marked as deleted rather than permanently removed

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify your DATABASE_URL is correct and accessible
2. **JWT Token Issues**: Ensure SECRET_KEY is properly set in environment variables
3. **Permission Errors**: Verify that users can only access their own resources
4. **Rate Limiting**: Check that requests are within the 100 requests/hour limit

### Enable Debug Logging
Add the following to your `.env` file:
```env
LOG_LEVEL=DEBUG
```

## Next Steps

1. Review the API documentation at `http://localhost:8000/docs` after starting the server
2. Explore the test suite to understand expected behaviors
3. Customize the models and endpoints as needed for your specific requirements