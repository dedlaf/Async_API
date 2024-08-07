import logging
from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

from .settings import GENRE_CACHE_EXPIRE_IN_SECONDS, BaseService


class GenreService(BaseService):
    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self.redis.object_from_cache(object_id=genre_id, key=Genre)
        if not genre:
            genre = await self._get_genre_from_es(genre_id)
            if not genre:
                return None
            await self.redis.put_object_to_cache(
                object_id=str(genre.id), key=genre, expire=GENRE_CACHE_EXPIRE_IN_SECONDS
            )

        return genre

    async def get_list(self, request: str) -> Optional[List[Genre]]:
        genres = await self.redis.objects_from_cache(object_id=request, key=Genre)
        genres = sorted(genres, key=lambda x: x.name)
        if not genres:
            genres = await self._get_list_from_es(request=request)
            if not genres:
                return []
        return genres

    async def _get_list_from_es(self, request: str) -> Optional[List[Genre]]:
        try:
            search_body = {
                "query": {"match_all": {}},
                "size": 10000,
                "sort": [{"name.keyword": {"order": "asc"}}],
            }
            response = await self.elastic.search(index="genres", body=search_body)
            genres = [Genre(**doc["_source"]) for doc in response["hits"]["hits"]]
            await self.redis.put_objects_to_cache(
                object_id=request, key=genres, expire=GENRE_CACHE_EXPIRE_IN_SECONDS
            )
            return genres

        except NotFoundError:
            logging.error(f"404 Not Found")
            return None

    async def _get_genre_from_es(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index="genres", id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc["_source"])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
