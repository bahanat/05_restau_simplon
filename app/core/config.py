from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
