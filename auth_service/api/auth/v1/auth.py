from datetime import timedelta

from fastapi import APIRouter, status, Depends, Response, Request

from db.redis import get_redis
from redis.asyncio import Redis
from schemas.user import UserCreateSchema, UserResponseSchema, UserLoginSchema, UserLogoutSchema
from services.user_services import UserService, get_user_service
from hash import hash_data
from core.config.components.token_conf import Tokens, get_tokens

router = APIRouter()


@router.post('/register', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    user.password = hash_data(user.password.encode())
    user_service.create_user(user)

    return user


@router.post("/login", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def login(
        user: UserLoginSchema,
        response: Response,
        request: Request,
        redis_client: Redis = Depends(get_redis),
        user_service: UserService = Depends(get_user_service),
        tokens: Tokens = Depends(get_tokens),
):
    user_service.login_user(user.login, user.password)

    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")
    access_token, refresh_token = await tokens.create(user)

    await redis_client.set(
        name=f"access_token:{user.login}:{hash_data(byte_agent)}", ex=timedelta(minutes=10), value=access_token
    )
    await redis_client.set(
        name=f"refresh_token:{user.login}:{hash_data(byte_agent)}", ex=timedelta(days=10), value=refresh_token
    )

    await tokens.set_in_cookies(access_token, refresh_token, response)

    return user


@router.post("/logout")
async def logout(
        user: UserLogoutSchema,
        request: Request,
        redis_client: Redis = Depends(get_redis),
):
    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")

    await redis_client.delete(f"access_token:{user.login}:{hash_data(byte_agent)}")
    await redis_client.delete(f"refresh_token:{user.login}:{hash_data(byte_agent)}")

    return user


@router.post("/logout_all")
async def logout_all(
        user: UserLogoutSchema,
        request: Request,
        redis_client: Redis = Depends(get_redis),
):
    async for key in redis_client.scan_iter(f"access_token:{user.login}:*"):
        await redis_client.delete(key)

    async for key in redis_client.scan_iter(f"refresh_token:{user.login}:*"):
        await redis_client.delete(key)

    return user
