# Secure Task API with User-Specific Data

This is a secure, user-specific RESTful API for managing tasks using Python FastAPI, SQLModel, and Neon PostgreSQL.

## Features

- Secure user authentication with JWT tokens
- User-specific task management (CRUD operations)
- Rate limiting (100 requests per hour per user)
- Soft deletion of tasks
- Proper data isolation (users can only access their own tasks)
- Comprehensive error handling

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- PyJWT
- bcrypt for password hashing

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows CMD: venv\Scripts\activate.bat
                             # On Windows PowerShell: venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables by copying `.env.example` to `.env` and updating the values
5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Troubleshooting

If you encounter a `ModuleNotFoundError` for FastAPI or other dependencies:

1. Ensure your virtual environment is activated:
   ```bash
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate     # On Windows CMD
   # or
   venv\Scripts\Activate.ps1 # On Windows PowerShell
   ```

2. If you get an execution policy error on Windows PowerShell, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Reinstall the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify the installation:
   ```bash
   python -c "import fastapi; print(fastapi.__version__)"
   ```

## Setup Scripts

Alternatively, you can use the provided setup scripts:

- On Linux/Mac: `./setup_backend.sh`
- On Windows CMD: `setup_backend.bat`
- On Windows PowerShell: `.\setup_backend.ps1` (after setting execution policy)

Then run the application:
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows CMD
# or
.\venv\Scripts\Activate.ps1 # Windows PowerShell

uvicorn main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Task Management
- `GET /api/users/{user_id}/tasks` - Get user's tasks
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Soft delete a task


## Running the Application

Choose one environment and stick with it:

### Option 1: Windows Environment
Open **Command Prompt** or **PowerShell**:
```cmd
# Activate virtual environment
venv\Scripts\Activate.bat

# Run the application
uvicorn main:app --reload
```

### Option 2: WSL/Linux Environment
Open **WSL Terminal** or **Linux Terminal**:
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

Note: The server runs in the terminal. Access the API endpoints in your browser or API client.
