from elasticsearch import AsyncElasticsearch
from redis import Redis

from .redis import RedisService


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch) -> None:
        self.redis = RedisService(redis)
        self.elastic = elastic


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5
PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5
