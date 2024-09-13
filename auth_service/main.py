from contextlib import asynccontextmanager

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.auth.v1 import auth, role, token_urls, user
from core.config.components.settings import Settings
from db import redis

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/auth/openapi",
    openapi_url="/auth/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(token_urls.router, prefix="/auth/token", tags=["token"])
app.include_router(role.router, prefix="/auth/role", tags=["roles"])
app.include_router(user.router, prefix="/auth/user", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8070)
