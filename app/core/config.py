from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
