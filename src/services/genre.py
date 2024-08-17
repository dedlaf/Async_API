from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from core.config.components.cache import AbstractCacheService, RedisService
from core.config.components.common_params import GENRE_CACHE_EXPIRE_IN_SECONDS
from core.config.components.storage import (AbstractStorageHandler,
                                            ElasticHandler)
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre


class GenreService:
    def __init__(
        self, cache: AbstractCacheService, storage_handler: AbstractStorageHandler
    ):
        self.cache = RedisService(cache)
        self.storage_handler = ElasticHandler(
            storage_handler,
            model=Genre,
            model_index="genres",
            search_query="name",
        )

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self.cache.get_object_from_cache(object_id=genre_id, key=Genre)
        if not genre:
            genre = await self.storage_handler.get_by_id(genre_id)
            if not genre:
                return None
            await self.cache.put_object_to_cache(
                object_id=str(genre.id), key=genre, expire=GENRE_CACHE_EXPIRE_IN_SECONDS
            )

        return genre

    async def get_list(self, request: str) -> Optional[List[Genre]]:
        genres = await self.cache.get_objects_from_cache(object_id=request, key=Genre)
        if not genres:
            genres = await self.storage_handler.get_list(request=request)
            if not genres:
                return []
        await self.cache.put_objects_to_cache(
            object_id=request, key=genres, expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )
        genres = sorted(genres, key=lambda x: x.name)
        return genres


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
