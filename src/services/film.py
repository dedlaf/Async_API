import logging
from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Request
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_list_of_films(
        self, request: str, sort=None, filters=None, query=None
    ) -> Optional[List[Film]]:
        films = await self._get_list_of_films_from_cache(request=request, sort=sort)

        if not films:
            films = await self._get_list_of_films_from_elastic(
                sort=sort, request=request, filters=filters, query=query
            )
            if not films:
                return []
        return films

    async def _get_list_of_films_from_cache(self, request: str, sort=None) -> Optional[List[Film]]:
        try:
            data = await self.redis.lrange(request, 0, -1)
            films = [Film.parse_raw(film) for film in data]
            if str(sort.get("sort"))[0] == "-":
                return sorted(films, key=lambda x: x.imdb_rating)
            return sorted(films, key=lambda x: x.imdb_rating, reverse=True)

        except Exception as e:
            logging.error(f"Error fetching films from Redis: {e}")
            return None

    async def _get_list_of_films_from_elastic(
        self, request: str, sort=None, filters=None, query=None
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

            search_body["sort"] = [{"imdb_rating": {"order": "desc"}}]

            if str(sort.get("sort"))[0] == "-":
                search_body["sort"] = [{"imdb_rating": {"order": "asc"}}]

            response = await self.elastic.search(index="movies", body=search_body)

            films = [Film(**doc["_source"]) for doc in response["hits"]["hits"]]
            for i in films:
                await self.redis.lpush(request, i.json())
            await self.redis.expire(request, FILM_CACHE_EXPIRE_IN_SECONDS)
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

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(str(film.id), film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
