from functools import wraps
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException, Request, Response, Header



async def check_access_token(cookies: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://nginx:80/api/v1/users/token/user", cookies=cookies
        ) as response:
            return response.status


async def check_refresh_token(cookies: dict):
    async with aiohttp.ClientSession() as refresh_session:
        async with refresh_session.get(
            "http://nginx:80/api/v1/users/token/refresh", cookies=cookies
        ) as refresh_response:
            return refresh_response.status, refresh_response.cookies

async def check_redis(cookies: dict, headers):
    print(cookies)
    async with aiohttp.ClientSession() as refresh_session:
        async with refresh_session.get(
                "http://nginx:80/api/v1/users/token/validate_token", cookies=cookies, headers=headers
        ) as refresh_response:
            return refresh_response.status

def verify_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        rq: Request = kwargs.get("request")
        rs: Response = kwargs.get("response")
        cookies = {
            "access_token_cookie": rq.cookies.get("access_token_cookie"),
            "refresh_token_cookie": rq.cookies.get("refresh_token_cookie"),
        }
        ans = await check_redis(cookies, rq.headers)
        if ans is HTTPStatus.OK.real:
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
        raise HTTPException(status_code=401, detail="Unauthorized")

    return wrapper
