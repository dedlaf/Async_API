import logging
from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

from .settings import PERSON_CACHE_EXPIRE_IN_SECONDS, BaseService


class PersonService(BaseService):
    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self.redis.object_from_cache(object_id=person_id, key=Person)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self.redis.put_object_to_cache(
                object_id=str(person.id),
                key=person,
                expire=PERSON_CACHE_EXPIRE_IN_SECONDS,
            )

        return person

    async def get_list(self, request: str, query: str) -> Optional[List[Person]]:
        persons = await self.redis.objects_from_cache(object_id=request, key=Person)
        persons = sorted(persons, key=lambda x: x.full_name)
        if not persons:
            persons = await self._get_list_from_es(request=request, query=query)
            if not persons:
                return []
        return persons

    async def _get_list_from_es(
        self, request: str, query: str
    ) -> Optional[List[Person]]:
        try:
            search_body = {
                "query": {"bool": {"must": [{"match": {"full_name": query}}]}},
                "size": 10000,
            }

            response = await self.elastic.search(index="persons", body=search_body)
            persons = [Person(**doc["_source"]) for doc in response["hits"]["hits"]]
            await self.redis.put_objects_to_cache(
                object_id=request, key=persons, expire=PERSON_CACHE_EXPIRE_IN_SECONDS
            )
            return persons

        except NotFoundError:
            logging.error(f"404 Not Found")
            return None

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index="persons", id=person_id)
        except NotFoundError:
            return None
        return Person(**doc["_source"])


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
