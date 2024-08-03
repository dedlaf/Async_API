import logging
from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Request
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


# TODO: Доработать класс с учетом готового ETL пайплайна
class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def get_list_of_persons(self, request: str, filters=None, query=None):
        persons = await self._get_list_of_persons_from_cache(request=request)

        if not persons:
            persons = await self._get_list_of_persons_from_elastic(
                filters=filters, request=request
            )
            if not persons:
                return []
        return persons

    async def _get_list_of_persons_from_cache(self, request: str):
        try:
            data = await self.redis.lrange(request, 0, -1)
            persons = [person.parse_raw(person) for person in data]
            return persons

        except Exception as e:
            print(f"Error fetching persons from Redis: {e}")
            return None

    async def _get_list_of_persons_from_elastic(
        self, request: str, filters=None, query=None
    ):
        try:

            search_body = {"query": {"match_all": {}}, "size": 10000}

            if query:
                search_body["query"] = {"bool": {"must": []}}
                search_body["query"]["bool"]["must"].append({"match": {"title": query}})

            response = await self.elastic.search(index="movies", body=search_body)
            # Извлекаем фильмы из результатов поиска
            persons = [Person(**doc["_source"]) for doc in response["hits"]["hits"]]
            for i in persons:
                await self.redis.lpush(request, i.json())
            return persons

        except NotFoundError:
            return None

    async def _person_from_cache(self, person_id):
        data = await self.redis.get(person_id)
        if not data:
            return None

        person = Person.parse_raw(data)
        return person

    async def _get_person_from_elastic(self, person_id: str):
        try:
            doc = await self.elastic.get(index="movies", id=person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])

    async def _put_person_to_cache(self, person: Person):

        await self.redis.set(
            str(person.id), person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
