import asyncio
from pprint import pprint

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from .fakedata.fake_data import FakeData
from .settings import test_settings

fake_data = FakeData()
bulk_query_movies, bulk_query_genres, bulk_query_persons = fake_data.transform_to_es(
    *fake_data.generate_data(100)
)


datas = [
    bulk_query_movies,
    bulk_query_persons,
    bulk_query_genres
]
indexes = [
    test_settings.es_index_movies,
    test_settings.es_index_persons,
    test_settings.es_index_genres,
]
mappings = [
    test_settings.es_index_mapping_film,
    test_settings.es_index_mapping_person,
    test_settings.es_index_mapping_genres,
]


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
def http_session_get(http_session: aiohttp.ClientSession):
    async def inner(url: str, query_data: dict = None) -> list:
        async with http_session.get("/api/v1/" + url, params=query_data) as response:
            pprint(response)
            return [await response.json(), response.headers, response.status]

    return inner


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_write_data(es_client: AsyncElasticsearch) -> None:
    for index, mapping, data in zip(indexes, mappings, datas):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(index=index, **mapping)
        updated, errors = await async_bulk(client=es_client, actions=data)
        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")
        await es_client.indices.refresh(index=index)
