import logging
from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

from .settings import FILM_CACHE_EXPIRE_IN_SECONDS, BaseService


class FilmService(BaseService):
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self.redis.object_from_cache(object_id=film_id, key=Film)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self.redis.put_object_to_cache(
                object_id=film_id, key=film, expire=FILM_CACHE_EXPIRE_IN_SECONDS
            )

        return film

    async def get_list(
        self, request: str, sort: dict = None, filters: dict = None, query: str = None
    ) -> Optional[List[Film]]:
        films = await self.redis.objects_from_cache(object_id=request, key=Film)
        films = sorted(films, key=lambda x: x.imdb_rating, reverse=True)
        if str(sort.get("sort"))[0] == "-":
            films = sorted(films, key=lambda x: x.imdb_rating)
        if not films:
            films = await self._get_list_from_es(
                sort=sort, request=request, filters=filters, query=query
            )
            if not films:
                return []
        return films

    async def _get_list_from_es(
        self, request: str, sort: dict = None, filters: dict = None, query: str = None
    ) -> Optional[List[Film]]:
        try:
            search_body = {
                "query": {"match_all": {}},
                "size": 10000,
            }

            if filters or query:
                search_body["query"] = {"bool": {"must": []}}

                if filters:
                    search_body["query"]["bool"]["must"].append(
                        {"match": {"genres": filters.get("filter")}}
                    )

                if query:
                    search_body["query"]["bool"]["must"].append(
                        {"match": {"title": query}}
                    )
            logging.info(search_body)
            search_body["sort"] = [{"imdb_rating": {"order": "desc"}}]

            if str(sort.get("sort"))[0] == "-":
                search_body["sort"] = [{"imdb_rating": {"order": "asc"}}]

            response = await self.elastic.search(index="movies", body=search_body)

            films = [Film(**doc["_source"]) for doc in response["hits"]["hits"]]
            await self.redis.put_objects_to_cache(
                object_id=request, key=films, expire=FILM_CACHE_EXPIRE_IN_SECONDS
            )
            return films

        except NotFoundError:
            logging.error(f"404 Not Found")
            return None

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
