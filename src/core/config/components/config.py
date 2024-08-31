import os
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config.components.logger import LOGGING


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "auth"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    ELASTIC_HOST: str = "elasticsearch"
    ELASTIC_PORT: int = 9200


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

logging_config.dictConfig(LOGGING)

PROJECT_NAME = settings.PROJECT_NAME

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

ELASTIC_HOST = settings.ELASTIC_HOST
ELASTIC_PORT = settings.ELASTIC_PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
