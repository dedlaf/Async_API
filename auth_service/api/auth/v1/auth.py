from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from hash import hash_data
from redis.asyncio import Redis

from core.config.components.token_conf import Tokens, get_tokens
from core.config.components.settings import settings
from db.redis import get_redis
from schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserLogoutSchema,
    UserResponseSchema,
)
from services.user_service import UserService, get_user_service
from requests_oauthlib import OAuth2Session
import requests
import random
import string
import aiohttp

router = APIRouter()


async def post_login_request(username: str, password: str, rs: Response) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://nginx:80/auth/login",
            json={"username": username, "password": password},
        ) as response:
            rs.set_cookie(
                key="access_token_cookie",
                value=response.cookies.get("access_token_cookie").value,
            )
            rs.set_cookie(
                key="refresh_token_cookie",
                value=response.cookies.get("refresh_token_cookie").value,
            )


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
)
async def register(
    user: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    user.password = hash_data(user.password.encode())
    user_service.create_user(user)

    return user


@router.post(
    "/login",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Log in to user account",
    description="Create new user session. Create new access and refresh tokens",
)
async def login(
    user: UserLoginSchema,
    response: Response,
    request: Request,
    redis_client: Redis = Depends(get_redis),
    user_service: UserService = Depends(get_user_service),
    tokens: Tokens = Depends(get_tokens),
):
    print(user)
    user_service.login_user(user.username, user.password)

    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")
    access_token, refresh_token = await tokens.create(user)

    await redis_client.set(
        name=f"access_token:{user.username}:{hash_data(byte_agent)}",
        ex=timedelta(minutes=10),
        value=access_token,
    )
    await redis_client.set(
        name=f"refresh_token:{user.username}:{hash_data(byte_agent)}",
        ex=timedelta(days=10),
        value=refresh_token,
    )

    await tokens.set_in_cookies(access_token, refresh_token, response)

    return user


@router.post(
    "/logout",
    summary="Log out of this user session",
    description="Delete access and refresh tokens of this session",
)
async def logout(
    user: UserLogoutSchema,
    request: Request,
    redis_client: Redis = Depends(get_redis),
):
    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")

    await redis_client.delete(f"access_token:{user.username}:{hash_data(byte_agent)}")
    await redis_client.delete(f"refresh_token:{user.username}:{hash_data(byte_agent)}")

    return user


@router.post(
    "/logout_all",
    summary="Log out of all user sessions",
    description="Delete all user's access and refresh tokens",
)
async def logout_all(
    user: UserLogoutSchema,
    request: Request,
    redis_client: Redis = Depends(get_redis),
):
    async for key in redis_client.scan_iter(f"access_token:{user.username}:*"):
        await redis_client.delete(key)

    async for key in redis_client.scan_iter(f"refresh_token:{user.username}:*"):
        await redis_client.delete(key)

    return user


@router.get("/login-yandex")
async def login_yandex():
    yandex = OAuth2Session(settings.yandex_client_id)
    authorization_url, _ = yandex.authorization_url("https://oauth.yandex.ru/authorize")
    return RedirectResponse(authorization_url)


@router.get("/callback-oauth")
async def callback_oauth(
    rs: Response, code: str, user_service: UserService = Depends(get_user_service)
):
    yandex_data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.yandex_client_id,
        "client_secret": settings.yandex_client_secret,
    }
    yandex_token_response = requests.post("https://oauth.yandex.ru/token", data=yandex_data)
    yandex_access_token = yandex_token_response.json().get("access_token")

    yandex_user_info_headers = {"Authorization": f"OAuth {yandex_access_token}"}
    yandex_user_info_response = requests.get(
        "https://login.yandex.ru/info?format=json", headers=yandex_user_info_headers
    )

    username = yandex_user_info_response.json().get("login")
    email = "email"
    password = yandex_user_info_response.json().get("psuid") + yandex_user_info_response.json().get("id")
    user = UserCreateSchema(username=username, email=email, password=hash_data(password.encode()))

    try:
        user_service.create_user(user)
        await post_login_request(username, password, rs)
        return "Successfully logged in"
    except HTTPException:
        await post_login_request(username, password, rs)
        return "Successfully logged in"
