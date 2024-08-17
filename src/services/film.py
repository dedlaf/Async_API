from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from core.config.components.base_service import (FILM_CACHE_EXPIRE_IN_SECONDS,
                                                 ElasticHandler, RedisService)
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film


class FilmService:
    def __init__(self, cache: Redis, storage_handler: ElasticHandler):
        self.cache = RedisService(cache)
        self.storage_handler = ElasticHandler(
            storage_handler,
            model=Film,
            model_index="movies",
            search_query="title",
            filter_query="genres",
        )

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self.cache.get_object_from_cache(object_id=film_id, key=Film)
        if not film:
            film = await self.storage_handler.get_by_id(film_id)
            if not film:
                return None
            await self.cache.put_object_to_cache(
                object_id=film_id, key=film, expire=FILM_CACHE_EXPIRE_IN_SECONDS
            )

        return film

    async def get_list(
        self, request: str, sort: dict = None, filters: dict = None, query: str = None
    ) -> Optional[List[Film]]:
        films = await self.cache.get_objects_from_cache(object_id=request, key=Film)

        if not films:
            films = await self.storage_handler.get_list(
                sort=sort, request=request, filters=filters, query=query
            )
            if not films:
                return []
        await self.cache.put_objects_to_cache(
            object_id=request, key=films, expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )
        films = sorted(films, key=lambda x: x.imdb_rating, reverse=True)
        if str(sort.get("sort"))[0] == "-":
            films = sorted(films, key=lambda x: x.imdb_rating)
        return films


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
