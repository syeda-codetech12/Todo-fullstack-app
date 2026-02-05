# Quickstart Guide: Todo Full-Stack Web App – Authentication & Security Focus

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (local or cloud instance)
- Git
- npm or yarn

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables (Backend)
Create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Run Database Migrations
```bash
cd backend
alembic revision --autogenerate -m Initial migration
alembic upgrade head
```

### 5. Frontend Setup
```bash
cd frontend
npm install
```

### 6. Environment Variables (Frontend)
Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

### 7. Run the Applications

#### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- POST /auth/register - Register a new user
- POST /auth/login - Login and get JWT tokens
- POST /auth/logout - Logout and invalidate session
- POST /auth/refresh - Refresh access token

### User Management
- GET /users/me - Get current user info
- PUT /users/me - Update current user info

### Tasks
- GET /tasks - Get current user's tasks
- POST /tasks - Create a new task
- GET /tasks/{id} - Get a specific task
- PUT /tasks/{id} - Update a specific task
- DELETE /tasks/{id} - Delete a specific task

## Security Features

### JWT Token Handling
- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Tokens are stored in httpOnly cookies for XSS protection
- All API requests require Authorization header with Bearer token

### Authorization
- Users can only access their own tasks
- API endpoints validate user identity against requested resources
- Proper HTTP status codes for unauthorized access (401, 403)

### Error Handling
- Standardized error response format
- Appropriate HTTP status codes
- User-friendly error messages without sensitive information exposure

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Deployment Notes
- Ensure HTTPS is enabled in production
- Set secure flags on cookies in production
- Use strong, randomly generated secrets
- Implement proper logging and monitoring
- Regular security audits of dependencies
