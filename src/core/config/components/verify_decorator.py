from functools import wraps
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException, Request, Response

async def check_access_token(cookies: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://nginx:80/auth/token/user", cookies=cookies
        ) as response:
            return response.status


async def check_refresh_token(cookies: dict):
    async with aiohttp.ClientSession() as refresh_session:
        async with refresh_session.get(
            "http://nginx:80/auth/token/refresh", cookies=cookies
        ) as refresh_response:
            return refresh_response.status, refresh_response.cookies


async def check_redis(cookies: dict, headers):
    async with aiohttp.ClientSession() as refresh_session:
        async with refresh_session.get(
                "http://nginx:80/auth/token/validate_token", cookies=cookies, headers=headers
        ) as refresh_response:
            if refresh_response.status is not HTTPStatus.OK.real:
                raise HTTPException(status_code=401, detail="Unauthorized")
            return refresh_response.status


async def has_user_role(cookies: dict, headers):
    async with aiohttp.ClientSession() as has_role_session:
        async with has_role_session.get(
                "http://nginx:80/auth/user/role/has_role", cookies=cookies, headers=headers
        ) as has_role_response:
            if has_role_response.status is not HTTPStatus.OK.real:
                raise HTTPException(status_code=401, detail="Unauthorized")
            return has_role_response.status


def verify_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rq: Request = kwargs.get("request")
        rs: Response = kwargs.get("response")
        cookies = {
            "access_token_cookie": rq.cookies.get("access_token_cookie"),
            "refresh_token_cookie": rq.cookies.get("refresh_token_cookie"),
        }

        await check_redis(cookies, rq.headers)

        if await check_access_token(cookies) is not HTTPStatus.OK.real:

            refresh_status, refreshed_cookies = await check_refresh_token(cookies)
            if refresh_status is HTTPStatus.OK.real:
                rs.set_cookie(
                    key="access_token_cookie",
                    value=refreshed_cookies.get("access_token_cookie").value,
                )
                rs.set_cookie(
                    key="refresh_token_cookie",
                    value=refreshed_cookies.get("refresh_token_cookie").value,
                )

                return await func(*args, **kwargs)

            raise HTTPException(status_code=401, detail="Unauthorized")

        return await func(*args, **kwargs)


    return wrapper


def has_role(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rq: Request = kwargs.get("request")
        rs: Response = kwargs.get("response")
        cookies = {
            "access_token_cookie": rq.cookies.get("access_token_cookie"),
            "refresh_token_cookie": rq.cookies.get("refresh_token_cookie"),
        }

        rs_status = await has_user_role(cookies, rq.headers)

        if not rs_status is HTTPStatus.OK.real:
            raise HTTPException(
                status_code=404,
                detail="Role not found",
            )

        return await func(*args, **kwargs)

    return wrapper
