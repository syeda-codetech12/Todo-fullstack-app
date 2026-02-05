@echo off
echo Setting up backend environment...
echo.

REM Check if venv exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Setup complete! Backend dependencies installed.
echo.
echo To start the backend server, run:
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --reload
echo.
pause
