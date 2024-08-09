import os
from logging import config as logging_config

from elasticsearch import AsyncElasticsearch
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis

from core.logger import LOGGING
from services.redis import RedisService


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "movies"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = "elasticsearch"
    ELASTIC_PORT: int = 9200


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch) -> None:
        self.redis = RedisService(redis)
        self.elastic = elastic


class CommonQueryParams:
    def __init__(self, page: int = 0, page_size: int = 50):
        self.page = page
        self.page_size = page_size
        self.offset_min = self.page * self.page_size
        self.offset_max = (self.page + 1) * self.page_size


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

logging_config.dictConfig(LOGGING)

PROJECT_NAME = settings.PROJECT_NAME

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

ELASTIC_HOST = settings.ELASTIC_HOST
ELASTIC_PORT = settings.ELASTIC_PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5
PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5
