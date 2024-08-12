import asyncio
from pprint import pprint

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from .settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="http_session", scope="session")
async def http_session():
    http_session = aiohttp.ClientSession(base_url=test_settings.service_url)
    yield http_session
    await http_session.close()


@pytest_asyncio.fixture(name="http_session_get")
def http_session_get(http_session):
    async def inner(url: str, query_data: dict = None):
        async with http_session.get(
            "/api/v1/" + url, params=query_data
        ) as response:
            pprint(response)
            return [await response.json(), response.headers, response.status]

    return inner


@pytest_asyncio.fixture(name="es_write_data")
def es_write_data(es_client):
    async def inner(data: list[dict], index, mapping):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(
            index=index, **mapping
        )

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")
        await es_client.indices.refresh(index=index)

    return inner
