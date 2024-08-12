import pytest
from redis import Redis

from ...settings import test_settings
from ..fakedata.fake_genre import FakeGenreData


redis = Redis(host=test_settings.redis_host)
redis.flushall()

genre_generator = FakeGenreData()
bulk_query = genre_generator.generate_genres(26)


@pytest.mark.asyncio
async def test_get_list(http_session_get, es_write_data):
    test_settings.es_page_size = len(bulk_query) if len(bulk_query) <= 1000 else 1000
    await es_write_data(
        bulk_query, test_settings.es_index_genres, test_settings.es_index_mapping_genres
    )
    body, headers, status = await http_session_get(
        "genres/"
    )
    assert status == 200
    assert len(body) == test_settings.es_page_size


@pytest.mark.asyncio
async def test_get_genre(http_session_get, es_write_data):
    await es_write_data(
        bulk_query,
        test_settings.es_index_persons,
        test_settings.es_index_mapping_person,
    )
    body, headers, status = await http_session_get(
        f"genres/{bulk_query[0].get('_id')}"
    )
    assert status == 200
    assert len(body) == 3


