import asyncio
import os

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()


async def get_redis_ready():
    redis = Redis(host=os.getenv("REDIS_HOST"), port=6379)

    while True:
        if await redis.ping():
            break
        await asyncio.sleep(1)
