from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from settings import settings

from api.v1 import bookmarks, likes, reviews, users
from models.like import Like
from models.review import Review
from models.user import User
from db import mongo
import logging
import sentry_sdk


sentry_sdk.init(
    dsn=settings.sentry_sdk,
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    client = AsyncIOMotorClient(settings.mongodb_uri)
    mongo.mongodb = client['someDb']
    await init_beanie(database=client.db_name, document_models=[Like, Review, User])
    yield
    client.close()

app = FastAPI(
    title=settings.project_name,
    docs_url="/mongo/openapi",
    openapi_url="/mongo/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/mongo/users", tags=["users"])
app.include_router(likes.router, prefix="/mongo/likes", tags=["likes"])
app.include_router(reviews.router, prefix="/mongo/reviews", tags=["reviews"])
app.include_router(bookmarks.router, prefix="/mongo/bookmarks", tags=["bookmarks"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
