from http import HTTPStatus

import pytest
from redis import Redis

from ..conftest import bulk_query_genres
from ..settings import test_settings

pytestmark = pytest.mark.asyncio

redis = Redis(host=test_settings.redis_host)
redis.flushall()


async def test_get_list(http_session_get: pytest.fixture) -> None:
    test_settings.es_page_size = (
        len(bulk_query_genres) if len(bulk_query_genres) <= 1000 else 1000
    )
    body, headers, status = await http_session_get("genres/")
    assert status == HTTPStatus.OK
    assert len(body) == test_settings.es_page_size


async def test_get_genre(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        f"genres/{bulk_query_genres[0].get('_id')}"
    )
    assert status == HTTPStatus.OK
    assert len(body) == 3


async def test_get_genre_404(http_session_get: pytest.fixture) -> None:
    body, headers, status = await http_session_get(
        "genres/bel45123;lsdkfjsdfk2tn3om4958ma5"
    )
    assert status == HTTPStatus.NOT_FOUND
