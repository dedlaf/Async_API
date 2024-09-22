from contextlib import asynccontextmanager

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from api.auth.v1 import auth, role, token_urls, user
from core.config.components.settings import Settings
from db import redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                username="web",
                agent_host_name="jaeger",
                agent_port=6831
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    yield
    await redis.redis.close()


configure_tracer()
limiter = Limiter(key_func=get_remote_address, default_limits=["1000/minute"])
app = FastAPI(
    title=settings.project_name,
    docs_url="/auth/openapi",
    openapi_url="/auth/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


FastAPIInstrumentor.instrument_app(app)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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
