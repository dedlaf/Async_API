from datetime import timedelta

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from hash import hash_data
from redis.asyncio import Redis

from core.config.components.settings import Settings
from core.config.components.token_conf import Tokens, get_tokens
from db.redis import get_redis
from schemas.user import UserResponseSchema
from services.user_service import UserService, get_user_service

router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


@router.get(
    "/refresh",
    summary="Update refresh and access tokens",
    description="Get refresh token from cookies. If token is valid, update access and refresh tokens pair, else return Unauthorized",
)
async def refresh(
    request: Request,
    response: Response,
    tokens: Tokens = Depends(get_tokens),
    user: UserService = Depends(get_user_service),
    redis_client: Redis = Depends(get_redis),
):
    user = user.get_user_by_username(await tokens.validate_refresh())
    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")
    access_token, refresh_token = await tokens.refresh(user=user, response=response)

    await redis_client.set(
        name=f"access_token:{user.username}:{hash_data(byte_agent)}",
        ex=timedelta(minutes=20),
        value=access_token,
    )
    await redis_client.set(
        name=f"refresh_token:{user.username}:{hash_data(byte_agent)}",
        ex=timedelta(days=10),
        value=refresh_token,
    )
    return {"msg": "Successfully logged in"}


@router.get("/user", summary="Get user from tokens", response_model=UserResponseSchema)
async def user(
    tokens: Tokens = Depends(get_tokens), user: UserService = Depends(get_user_service)
):
    current_user = await tokens.validate()

    current_user = user.get_user_by_username(current_user)
    return current_user


@router.get(
    "/validate_token",
    summary="Check for tokens in redis",
    description="Get refresh token, then check if this token exists in redis. If token does not exist return Unauthorized, else return Success",
)
async def check_redis(
    request: Request,
    redis: Redis = Depends(get_redis),
    tokens: Tokens = Depends(get_tokens),
    user: UserService = Depends(get_user_service),
):
    refresh_token = request.cookies.get("refresh_token_cookie")
    user = user.get_user_by_username(await tokens.validate())
    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")
    rf_in_redis = await redis.get(
        f"refresh_token:{user.username}:{hash_data(byte_agent)}"
    )
    if rf_in_redis:
        if rf_in_redis.decode() == str(refresh_token):
            return {"msg": "Successfully validation"}
    raise HTTPException(status_code=401, detail="Unauthorized")
