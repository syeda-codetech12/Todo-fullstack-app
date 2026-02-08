#!/usr/bin/env python3
"""
Server runner for the Secure Task API.

This script starts the FastAPI application using uvicorn without the reload
option to prevent unexpected shutdowns that can occur with file watching
in certain environments.
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting Secure Task API server...")
    print("Visit http://127.0.0.1:8000/docs for API documentation")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
