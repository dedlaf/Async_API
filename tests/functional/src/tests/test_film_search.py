import pytest
from redis import Redis

from ..settings import test_settings
from ..conftest import bulk_query_movies

redis = Redis(host=test_settings.redis_host)
redis.flushall()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "query": movie.get("_source").get("title"),
                "page_size": test_settings.es_page_size,
            },
            {"status": 200, "length": 1},
        )
        for movie in bulk_query_movies
    ],
)
@pytest.mark.asyncio
async def test_search(http_session_get, query_data, expected_answer):
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == 200
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_list(http_session_get):
    test_settings.es_page_size = len(bulk_query_movies) if len(bulk_query_movies) <= 1000 else 1000
    body, headers, status = await http_session_get(
        "films/", {"page_size": test_settings.es_page_size}
    )
    assert status == 200
    assert len(body) == test_settings.es_page_size


@pytest.mark.asyncio
async def test_get_film(http_session_get):
    body, headers, status = await http_session_get(f'films/{bulk_query_movies[0].get("_id")}')
    assert status == 200
    assert len(body) == 9
