from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://puzzleuser:puzzlepass@db:5432/puzzledb"
    SECRET_KEY: str = "your-very-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

settings = Settings()
