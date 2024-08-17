import abc
import logging
from typing import List, Optional, Type

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from redis import Redis

from models.film import Film


class AbstractStorageHandler(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, *args, **kwargs): ...

    @abc.abstractmethod
    def get_list(self, *args, **kwargs): ...


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    def get_object_from_cache(self, *args, **kwargs): ...

    @abc.abstractmethod
    def put_object_to_cache(self, *args, **kwargs): ...

    @abc.abstractmethod
    def get_objects_from_cache(self, *args, **kwargs): ...

    @abc.abstractmethod
    def put_objects_to_cache(self, *args, **kwargs): ...


class ElasticHandler(AbstractStorageHandler):
    def __init__(
        self,
        elastic: AsyncElasticsearch,
        model,
        model_index,
        search_query,
        filter_query,
    ):
        self.elastic = elastic
        self.model = model
        self.model_index = model_index
        self.search_query = search_query
        self.filter_query = filter_query

    async def get_by_id(self, model_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index=self.model_index, id=model_id)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    async def get_list(
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
                        {"match": {self.filter_query: filters.get("filter")}}
                    )

                if query:
                    search_body["query"]["bool"]["must"].append(
                        {"match": {self.search_query: query}}
                    )

            response = await self.elastic.search(
                index=self.model_index, body=search_body
            )

            data = [self.model(**doc["_source"]) for doc in response["hits"]["hits"]]

            return data

        except NotFoundError:
            logging.error("404 Not Found")
            return None


class RedisService(AbstractCache):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get_object_from_cache(
        self, object_id: str, key: Type[BaseModel]
    ) -> Optional[BaseModel]:
        data = await self.redis.get(object_id)
        if not data:
            return None

        final_data = key.parse_raw(data)
        return final_data

    async def put_object_to_cache(
        self, object_id: str, key: Type[BaseModel], expire: int = 5 * 60
    ) -> None:
        await self.redis.set(object_id, key.json(), expire)

    async def get_objects_from_cache(
        self, object_id: str, key: Type[BaseModel]
    ) -> Optional[BaseModel]:
        try:
            data = await self.redis.lrange(object_id, 0, -1)
            final_data = [key.parse_raw(data_object) for data_object in data]
            return final_data

        except Exception as e:
            logging.error(f"Error fetching genres from Redis: {e}")
            return None

    async def put_objects_to_cache(
        self, object_id: str, key: List[BaseModel], expire: int = 5 * 60
    ) -> None:
        for i in key:
            await self.redis.lpush(object_id, i.json())
        await self.redis.expire(object_id, expire)


class CommonQueryParams:
    def __init__(self, page: int = 0, page_size: int = 50):
        self.page = page
        self.page_size = page_size
        self.offset_min = self.page * self.page_size
        self.offset_max = (self.page + 1) * self.page_size


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5
PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5
