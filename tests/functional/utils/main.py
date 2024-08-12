import asyncio
from time import sleep

from wait_for_es import get_es_ready
from wait_for_redis import get_redis_ready

if __name__ == "__main__":
    get_es_ready()
    asyncio.run(get_redis_ready())
    print("Redis and Elasticsearch are ready")
