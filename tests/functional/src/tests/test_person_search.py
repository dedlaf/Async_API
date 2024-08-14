import pytest
from redis import Redis

from ..conftest import bulk_query_persons
from ..settings import test_settings

redis = Redis(host=test_settings.redis_host)
redis.flushall()


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "query": person.get("_source").get("full_name"),
                "page_size": test_settings.es_page_size,
            },
            {"status": 200, "length": 1},
        )
        for person in bulk_query_persons
    ],
)
@pytest.mark.asyncio
async def test_search(http_session_get, query_data, expected_answer):
    print(bulk_query_persons)
    body, headers, status = await http_session_get("persons/search/", query_data)
    assert status == 200
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_person(http_session_get):
    body, headers, status = await http_session_get(
        f"persons/{bulk_query_persons[0].get('_id')}"
    )
    assert status == 200
    assert len(body) == 3


@pytest.mark.asyncio
async def test_get_person_404(http_session_get):
    body, headers, status = await http_session_get(
        "persons/qregfqowe'uj'p9ujr4'[0p29u3"
    )
    assert status == 404


@pytest.mark.asyncio
async def test_get_person_film(http_session_get):
    body, headers, status = await http_session_get(
        f"persons/{bulk_query_persons[0].get('_id')}/film"
    )
    assert status == 200
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_person_film_404(http_session_get):
    body, headers, status = await http_session_get(
        "persons/qregfqowe'uj'p9ujr4'[0p29u3/film"
    )
    assert status == 404
