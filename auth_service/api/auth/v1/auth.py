from datetime import timedelta

import aiohttp
from core.config.components.token_conf import Tokens, get_tokens
from db.redis import get_redis
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from hash import hash_data
from redis.asyncio import Redis

from requests_oauthlib import OAuth2Session

from core.config.components.settings import settings
from core.config.components.token_conf import Tokens, get_tokens
from db.redis import get_redis
from schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserLogoutSchema,
    UserResponseSchema,
    UserResponseAdminSchema,
)

from services.oauth_service import OauthService, get_oauth_service
from services.user_service import UserService, get_user_service

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
    response_model=UserResponseAdminSchema,
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
    user_agent = request.headers.get("user-agent")
    user = user_service.login_user(user.username, user.password, user_agent)

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
    redis_client: Redis = Depends(get_redis),
):
    async for key in redis_client.scan_iter(f"access_token:{user.username}:*"):
        await redis_client.delete(key)

    async for key in redis_client.scan_iter(f"refresh_token:{user.username}:*"):
        await redis_client.delete(key)

    return user


@router.get("/login-oauth")
async def login_oauth(provider, oauth: OauthService = Depends(get_oauth_service)):
    if provider == "yandex":
        url = oauth.get_authorization_url_yandex()
        return RedirectResponse(url)
    elif provider == "vk":
        url = oauth.get_authorization_url_vk()
        return RedirectResponse(url)


@router.get("/callback-vk")
async def callback_vk(
    rs: Response,
    code: str,
    state,
    device_id,
    user_service: UserService = Depends(get_user_service),
    oauth: OauthService = Depends(get_oauth_service),
):
    user_info = await oauth.get_user_vk(code=code, state=state, device_id=device_id)
    username = user_info.get("user").get("user_id")
    email = "email"
    password = "password"
    user = UserCreateSchema(
        username=username, email=email, password=hash_data(password.encode())
    )

    try:
        user_service.create_user(user)
        user = user_service.get_user_by_username(username)
        user_service.create_social_user(
            user=user,
            social_type="vk",
            social_user_id=user_info.get("user").get("user_id"),
        )
        await post_login_request(username, password, rs)
        return "Successfully logged in"
    except HTTPException:
        await post_login_request(username, password, rs)
        return "Successfully logged in"


@router.get("/callback-yandex")
async def callback_yandex(
    rs: Response,
    code: str,
    user_service: UserService = Depends(get_user_service),
    oauth: OauthService = Depends(get_oauth_service),
):
    user_info = await oauth.get_user_yandex(code=code)
    username = user_info.get("login")
    email = "email"
    password = "password"
    user = UserCreateSchema(
        username=username, email=email, password=hash_data(password.encode())
    )
    try:
        user_service.create_user(user)
        user = user_service.get_user_by_username(username)
        user_service.create_social_user(
            user=user, social_type="yandex", social_user_id=user_info.get("id")
        )
        await post_login_request(username, password, rs)
        return "Successfully logged in"
    except HTTPException:
        await post_login_request(username, password, rs)
        return "Successfully logged in"
