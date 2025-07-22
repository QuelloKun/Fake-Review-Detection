from typing import Optional, List
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fake Review Detection API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: PostgresDsn
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ML Model
    MODEL_PATH: str = "./models/"
    MODEL_NAME: str = "classifierx.pickle"
    CACHE_TTL: int = 3600
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    @validator("DATABASE_URL", pre=True)
    def build_database_url(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username="user",
            password="password",
            host="localhost",
            port=5432,
            path="fake_reviews",
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
