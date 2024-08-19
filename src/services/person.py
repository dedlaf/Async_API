from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from core.config.components.cache import AbstractCacheService, RedisService
from core.config.components.common_params import PERSON_CACHE_EXPIRE_IN_SECONDS
from core.config.components.storage import (AbstractStorageHandler,
                                            ElasticHandler)
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person


class PersonService:
    def __init__(
        self, cache: AbstractCacheService, storage_handler: AbstractStorageHandler
    ):
        self.cache = cache
        self.storage_handler = storage_handler

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self.cache.get_object_from_cache(object_id=person_id, key=Person)
        if not person:
            person = await self.storage_handler.get_by_id(person_id)
            if not person:
                return None
            await self.cache.put_object_to_cache(
                object_id=str(person.id),
                key=person,
                expire=PERSON_CACHE_EXPIRE_IN_SECONDS,
            )

        return person

    async def get_list(self, request: str, query: str) -> Optional[List[Person]]:
        persons = await self.cache.get_objects_from_cache(object_id=request, key=Person)
        if not persons:
            persons = await self.storage_handler.get_list(request=request, query=query)
            if not persons:
                return []
        await self.cache.put_objects_to_cache(
            object_id=request, key=persons, expire=PERSON_CACHE_EXPIRE_IN_SECONDS
        )
        persons = sorted(persons, key=lambda x: x.full_name)
        return persons


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(
        RedisService(redis),
        ElasticHandler(
            elastic,
            model=Person,
            model_index="persons",
            search_query="full_name",
        ),
    )
