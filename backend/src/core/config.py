from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ABS_PATH = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    DB_URL: str
    DB_POOL_SIZE: int
    DB_POOL_TIMEOUT: int
    DB_POOL_RECYCLE: int
    DB_POOL_PRE_PING: bool

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=ABS_PATH / ".env", extra="ignore")


settings = Settings()  # type: ignore
