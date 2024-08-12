import pytest
from redis import Redis

from ...settings import test_settings
from ..fakedata.fake_genre import FakeGenreData
from ..fakedata.fake_movie import FakeMovieData
from ..fakedata.fake_person import FakePersonData

redis = Redis(host=test_settings.redis_host)
redis.flushall()

movie_generator = FakeMovieData(FakePersonData(), FakeGenreData())
bulk_query = movie_generator.generate_movies(1)


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
        for movie in bulk_query
    ],
)
@pytest.mark.asyncio
async def test_search(http_session_get, es_write_data, query_data, expected_answer):
    await es_write_data(
        bulk_query, test_settings.es_index_movies, test_settings.es_index_mapping_film
    )
    body, headers, status = await http_session_get("films/search/", query_data)
    assert status == 200
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_list(http_session_get, es_write_data):
    test_settings.es_page_size = len(bulk_query) if len(bulk_query) <= 1000 else 1000
    await es_write_data(
        bulk_query, test_settings.es_index_movies, test_settings.es_index_mapping_film
    )
    body, headers, status = await http_session_get(
        "films/", {"page_size": test_settings.es_page_size}
    )
    assert status == 200
    assert len(body) == test_settings.es_page_size


@pytest.mark.asyncio
async def test_get_film(http_session_get, es_write_data):
    await es_write_data(
        bulk_query, test_settings.es_index_movies, test_settings.es_index_mapping_film
    )
    body, headers, status = await http_session_get(f'films/{bulk_query[0].get("_id")}')
    assert status == 200
    assert len(body) == 9
