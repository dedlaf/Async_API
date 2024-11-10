import logging
from contextlib import asynccontextmanager

import aio_pika
from api.v1 import welcome_email, content_crud, template_crud, event_crud
from core.settings import settings
from db import rabbitmq, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host="localhost", port=6379)
    print(redis.redis)
    rabbitmq.rabbitmq = await aio_pika.connect_robust(
        host="rabbitmq", login="dedlaf", password="123qwe", port=5672
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
    lifespan=lifespan,
)

logger = logging.getLogger("api_logger")
logger.info("Starting")


app.include_router(welcome_email.router, prefix="/welcome", tags=["welcome-email"])
app.include_router(template_crud.router, prefix="/templates", tags=["template_crud"])
app.include_router(content_crud.router, prefix="/contents", tags=["content_crud"])
app.include_router(event_crud.router, prefix="/events", tags=["events_crud"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
