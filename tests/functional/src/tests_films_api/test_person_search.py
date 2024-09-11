from http import HTTPStatus
from typing import Any

import pytest
from redis import Redis

from .conftest import bulk_query_persons
from .settings import test_settings

pytestmark = pytest.mark.asyncio

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
async def test_search(
    http_session_get: pytest.fixture,
    query_data: dict[str, Any],
    expected_answer: dict[str, int],
) -> None:
    print(bulk_query_persons)
    body, headers, status = await http_session_get("persons/search/", query_data)
    assert status == HTTPStatus.OK
    assert len(body) > 0


async def test_get_person(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        f"persons/{bulk_query_persons[0].get('_id')}"
    )
    assert status == HTTPStatus.OK
    assert len(body) == 3


async def test_get_person_404(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        "persons/qregfqowe'uj'p9ujr4'[0p29u3"
    )
    assert status == HTTPStatus.NOT_FOUND


async def test_get_person_film(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        f"persons/{bulk_query_persons[0].get('_id')}/film"
    )
    assert status == HTTPStatus.OK
    assert len(body) > 0


async def test_get_person_film_404(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        "persons/qregfqowe'uj'p9ujr4'[0p29u3/film"
    )
    assert status == HTTPStatus.NOT_FOUND
