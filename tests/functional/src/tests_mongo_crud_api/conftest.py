import asyncio
from pprint import pprint

import aiohttp
import pytest_asyncio

from .fakedata.data import DataSeeder

count = 50
_db_name = "someDb"
data_seeder = DataSeeder(_db_name=_db_name, count=count)
data_seeder.clear_all_collections()
user, review, like = data_seeder.seed_all()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="http_session", scope="session")
async def http_session():
    http_session = aiohttp.ClientSession(base_url="http://nginx")
    yield http_session
    await http_session.close()


@pytest_asyncio.fixture(name="http_session_delete")
def http_session_delete(http_session: aiohttp.ClientSession) -> callable:
    async def inner(url: str, data: dict = None) -> list:
        async with http_session.delete(url, json=data) as response:
            pprint(response)
            return [
                await response.json(),
                response.headers,
                response.status,
                response.cookies,
            ]

    return inner


@pytest_asyncio.fixture(name="http_session_put")
def http_session_put(http_session: aiohttp.ClientSession) -> callable:
    async def inner(url: str, data: dict = None) -> list:
        async with http_session.put(url, json=data) as response:
            pprint(response)
            return [
                await response.json(),
                response.headers,
                response.status,
                response.cookies,
            ]

    return inner


@pytest_asyncio.fixture(name="http_session_get")
def http_session_get(http_session: aiohttp.ClientSession) -> callable:
    async def inner(url: str, query_data: dict = None) -> list:
        async with http_session.get(url, params=query_data) as response:
            pprint(response)
            return [
                await response.json(),
                response.headers,
                response.status,
                response.cookies,
            ]

    return inner


@pytest_asyncio.fixture(name="http_session_post")
def http_session_post(http_session: aiohttp.ClientSession) -> callable:
    async def inner(url: str, query_data: dict = None, json: dict = None) -> list:
        async with http_session.post(url, params=query_data, json=json) as response:
            pprint(response)
            return [
                await response.json(),
                response.headers,
                response.status,
                response.cookies,
            ]

    return inner
