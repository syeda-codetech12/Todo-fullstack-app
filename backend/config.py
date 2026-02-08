from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    # Use a local SQLite database by default for easier local development.
    # If NEON_DATABASE_URL or DATABASE_URL is set, those will override this.
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./task_api_dev.db")
    neon_database_url: Optional[str] = os.getenv("NEON_DATABASE_URL")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-here-make-it-long-and-random")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "4000")) 
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Rate limiting
    rate_limit_requests: int = 1000  # requests per hour per user (increased for development)
    rate_limit_window: int = 3600  # in seconds (1 hour)

    # Application settings
    app_name: str = "Secure Task API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"

settings = Settings()