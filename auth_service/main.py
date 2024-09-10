from contextlib import asynccontextmanager

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.auth.v1 import auth, role, token_urls
from core.config.components import settings
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/v1/users/openapi",
    openapi_url="/api/v1/users/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(token_urls.router, prefix="/api/v1/users/token", tags=["auth"])
app.include_router(role.router, prefix="/api/v1/users/roles", tags=["roles"])
app.include_router(auth.router, prefix="/api/v1/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8070)
