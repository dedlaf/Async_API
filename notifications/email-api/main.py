from contextlib import asynccontextmanager

from db import redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from core.settings import settings
import aio_pika
from api.v1 import welcome_email
from db import rabbitmq

import logging

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host='localhost', port=6379)
    print(redis.redis)
    rabbitmq.rabbitmq = await aio_pika.connect_robust(
        host='localhost',
        login='dedlaf',
        password='123qwe',
        port=5672
    )
    channel = await rabbitmq.rabbitmq.channel()
    queue = await channel.declare_queue("welcome_email", durable=True)
    print(type(queue))
    print(type(channel))
    print(type(rabbitmq.rabbitmq))

    yield
    await rabbitmq.rabbitmq.close()
    await redis.redis.close()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

logger = logging.getLogger("api_logger")
logger.info('Starting')


app.include_router(welcome_email.router, prefix="", tags=["welcome-email"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
