import logging
from typing import List, Optional, Type

from pydantic import BaseModel
from redis.asyncio import Redis


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def object_from_cache(
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

    async def objects_from_cache(
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
