import asyncio
import os
import time

from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()


async def get_redis_ready():
    print("Starting elasticsearch")
    redis = Redis(host=os.getenv("REDIS_HOST"), port=6379)

    while True:
        if await redis.ping():
            print("Redis ready")
            break
        await asyncio.sleep(1)
