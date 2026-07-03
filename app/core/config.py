import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "QRKot"
    app_description: str = "Благотворительный фонд поддержки котиков"
    
    @property
    def database_url(self) -> str:
        if os.getenv("PYTEST_CURRENT_TEST"):
            return "sqlite+aiosqlite:///:memory:"
        return "sqlite+aiosqlite:///./fastapi.db"

    class Config:
        env_file = ".env"


settings = Settings()
