#!/bin/bash
echo "Setting up backend environment..."
echo ""

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "Setup complete! Backend dependencies installed."
echo ""
echo "To start the backend server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
