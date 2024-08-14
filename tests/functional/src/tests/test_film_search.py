import pytest
from redis import Redis

from ..conftest import bulk_query_genres, bulk_query_movies
from ..settings import test_settings

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
@pytest.mark.asyncio
async def test_search(http_session_get, query_data):
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == 200
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
@pytest.mark.asyncio
async def test_get_list_pagination(http_session_get, page, page_size, expected_answer):
    body, headers, status = await http_session_get(
        "films/", {"page": page, "page_size": page_size}
    )
    assert status == 200
    assert len(body) == expected_answer


@pytest.mark.parametrize(
    "page, page_size, expected_answer",
    (
        [
            (1000, 1000, 404),
            (20, 3424, 404),
            (-50123, 1, 404),
            ("second", 50, 422),
        ]
    ),
)
@pytest.mark.asyncio
async def test_get_list_pagination_404(
    http_session_get, page, page_size, expected_answer
):
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
@pytest.mark.asyncio
async def test_get_list_filter(http_session_get, query_data):
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == 200
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
@pytest.mark.asyncio
async def test_get_list_filter_404(http_session_get, query_data):
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == 404
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_list(http_session_get):
    test_settings.es_page_size = (
        len(bulk_query_movies) if len(bulk_query_movies) <= 1000 else 1000
    )
    body, headers, status = await http_session_get(
        "films/", {"page_size": test_settings.es_page_size}
    )
    assert status == 200
    assert len(body) == test_settings.es_page_size


@pytest.mark.asyncio
async def test_get_film(http_session_get):
    body, headers, status = await http_session_get(
        f'films/{bulk_query_movies[0].get("_id")}'
    )
    assert status == 200
    assert len(body) == 9


@pytest.mark.asyncio
async def test_get_film_404(http_session_get):
    body, headers, status = await http_session_get("films/ldfgahlkjhlqknf;2141afwgtel")
    assert status == 404
