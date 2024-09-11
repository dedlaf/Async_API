from http import HTTPStatus
from typing import Any

import pytest
from redis import Redis

from .conftest import bulk_query_genres, bulk_query_movies
from .settings import test_settings

pytestmark = pytest.mark.asyncio

redis = Redis(host=test_settings.redis_host)
redis.flushall()


@pytest.mark.parametrize(
    "query_data",
    [
        {
            "query": movie.get("_source").get("title"),
            "page_size": test_settings.es_page_size,
        }
        for movie in bulk_query_movies
    ],
)
async def test_search(
    http_session_get: pytest.fixture, query_data: list[dict[str, Any]]
) -> None:
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == HTTPStatus.OK
    assert len(body) > 0


@pytest.mark.parametrize(
    "page, page_size, expected_answer",
    (
        [
            (0, 20, 20),
            (20, 4, 4),
            (50, 1, 1),
            (1, 50, 50),
        ]
    ),
)
async def test_get_list_pagination(
    http_session_get: pytest.fixture, page: int, page_size: int, expected_answer: int
) -> None:
    body, headers, status = await http_session_get(
        "films/", {"page": page, "page_size": page_size}
    )
    assert status == HTTPStatus.OK
    assert len(body) == expected_answer


@pytest.mark.parametrize(
    "page, page_size, expected_answer",
    (
        [
            (1000, 1000, HTTPStatus.NOT_FOUND),
            (20, 3424, HTTPStatus.NOT_FOUND),
            (-50123, 1, HTTPStatus.NOT_FOUND),
            ("second", 50, HTTPStatus.UNPROCESSABLE_ENTITY),
        ]
    ),
)
async def test_get_list_pagination_404(
    http_session_get: pytest.fixture, page: int, page_size: int, expected_answer: int
) -> None:
    body, headers, status = await http_session_get(
        "films/", {"page": page, "page_size": page_size}
    )
    assert status == expected_answer


@pytest.mark.parametrize(
    "query_data",
    [
        {
            "filter": genre.get("_source").get("name"),
            "sort": "-imdb_rating",
            "page_size": test_settings.es_page_size,
        }
        for genre in bulk_query_genres[:50]
    ],
)
async def test_get_list_filter(
    http_session_get: pytest.fixture, query_data: list[dict[str, Any]]
) -> None:
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == HTTPStatus.OK
    assert len(body) > 0


@pytest.mark.parametrize(
    "query_data",
    [
        {
            "filter": "adfkmasjkdfh2ou",
            "sort": "-imdb_rating",
            "page_size": test_settings.es_page_size,
        }
    ],
)
async def test_get_list_filter_404(
    http_session_get: pytest.fixture, query_data: list[dict[str, Any]]
) -> None:
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == HTTPStatus.NOT_FOUND
    assert len(body) > 0


async def test_get_list(http_session_get: pytest.fixture) -> None:
    test_settings.es_page_size = (
        len(bulk_query_movies) if len(bulk_query_movies) <= 1000 else 1000
    )
    body, headers, status = await http_session_get(
        "films/", {"page_size": test_settings.es_page_size}
    )
    assert status == HTTPStatus.OK
    assert len(body) == test_settings.es_page_size


async def test_get_film(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        f'films/{bulk_query_movies[0].get("_id")}'
    )
    assert status == HTTPStatus.OK
    assert len(body) == 9


async def test_get_film_404(http_session_get) -> None:
    body, headers, status = await http_session_get("films/ldfgahlkjhlqknf;2141afwgtel")
    assert status == HTTPStatus.NOT_FOUND
