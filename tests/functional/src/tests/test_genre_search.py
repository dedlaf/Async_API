import pytest
from redis import Redis

from ..conftest import bulk_query_genres
from ..settings import test_settings
import aiohttp

redis = Redis(host=test_settings.redis_host)
redis.flushall()


@pytest.mark.asyncio
async def test_get_list(http_session_get: aiohttp.ClientSession) -> None:
    test_settings.es_page_size = (
        len(bulk_query_genres) if len(bulk_query_genres) <= 1000 else 1000
    )
    body, headers, status = await http_session_get("genres/")
    assert status == 200
    assert len(body) == test_settings.es_page_size


@pytest.mark.asyncio
async def test_get_genre(http_session_get: aiohttp.ClientSession) -> None:
    body, headers, status = await http_session_get(
        f"genres/{bulk_query_genres[0].get('_id')}"
    )
    assert status == 200
    assert len(body) == 3


@pytest.mark.asyncio
async def test_get_genre_404(http_session_get: aiohttp.ClientSession) -> None:
    body, headers, status = await http_session_get(
        "genres/bel45123;lsdkfjsdfk2tn3om4958ma5"
    )
    assert status == 404
