from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from settings import Settings
from api.v1 import mongo_crud
from db import mongo

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient('localhost', 27017)
    mongo.mongodb = app.mongodb_client['UsersDB']
    yield
    await app.mongodb_client.close()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(mongo_crud.router, prefix="/users", tags=["hello"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8050)
