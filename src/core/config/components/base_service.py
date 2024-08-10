from elasticsearch import AsyncElasticsearch
from redis import Redis

from services.redis import RedisService


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


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5
PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5
