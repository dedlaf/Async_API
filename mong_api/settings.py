import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    project_name: str = "auth"

    redis_host: str = "redis"
    redis_port: int = 6379


settings = Settings(_env_file=".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
