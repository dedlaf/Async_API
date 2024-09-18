from datetime import timedelta

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from hash import hash_data
from redis.asyncio import Redis

from core.config.components.token_conf import Tokens, get_tokens
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


router = APIRouter()

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

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
async def login_yandex(
    response: Response,

):
    client_id = ''
    redirect_uri = 'http://localhost/auth/callback-oauth'

    yandex = OAuth2Session(client_id, redirect_uri=redirect_uri)

    authorization_url, state = yandex.authorization_url('https://oauth.yandex.ru/authorize')

    return RedirectResponse(authorization_url)

@router.get("/callback-oauth")
async def callback_oauth(
    code: str,
    user_service: UserService = Depends(get_user_service)
):
    client_id = ''
    client_secret = ''
    redirect_uri = 'http://localhost/api/v1/films'
    token_url = 'https://oauth.yandex.ru/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_url, data=payload)

    token = response.json().get("access_token")
    url = "https://login.yandex.ru/info?format=json"

    headers = {"Authorization": f"OAuth {token}"}
    response = requests.get(url, headers=headers)

    response_json = response.json()
    username = response_json.get("login")
    email = "email"
    password = generate_password()
    user = UserCreateSchema(username=username, email=email, password=hash_data(password.encode()))
    try:
        user_service.create_user(user)
    except:
        return RedirectResponse('http://localhost/auth/films')


    return {"username: ": username, "email: ": email, "password": password}