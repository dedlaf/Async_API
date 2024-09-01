from contextlib import asynccontextmanager

import psycopg2
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from psycopg2.extras import RealDictCursor
from redis.asyncio import Redis

from api.auth.v1 import token_urls, role
from core.config.components import settings
from core.config.components.settings import DSL
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    conn = psycopg2.connect(**DSL, cursor_factory=RealDictCursor)

    yield
    yield
    await redis.redis.close()
    await conn.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/v1/auth/openapi",
    openapi_url="/api/v1/auth/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(token_urls.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(role.router, prefix="/roles", tags=["roles"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8070)
