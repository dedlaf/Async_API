import pytest
from redis import Redis

from ...settings import test_settings
from ..fakedata.fake_genre import FakeGenreData
from ..fakedata.fake_movie import FakeMovieData
from ..fakedata.fake_person import FakePersonData

redis = Redis(host=test_settings.redis_host)
redis.flushall()

person_generator = FakePersonData()
movie_generator = FakeMovieData(FakePersonData(), FakeGenreData())
bulk_query = person_generator.generate_people(1)


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
        for person in bulk_query
    ],
)
@pytest.mark.asyncio
async def test_search(http_session_get, es_write_data, query_data, expected_answer):
    await es_write_data(
        bulk_query,
        test_settings.es_index_persons,
        test_settings.es_index_mapping_person,
    )
    body, headers, status = await http_session_get("persons/search/", query_data)
    assert status == 200
    assert len(body) > 0


@pytest.mark.asyncio
async def test_get_person(http_session_get, es_write_data):
    await es_write_data(
        bulk_query,
        test_settings.es_index_persons,
        test_settings.es_index_mapping_person,
    )
    body, headers, status = await http_session_get(
        f"persons/{bulk_query[0].get('_id')}"
    )
    assert status == 200
    assert len(body) == 3


@pytest.mark.asyncio
async def test_get_person_film(http_session_get, es_write_data):
    await es_write_data(
        bulk_query,
        test_settings.es_index_persons,
        test_settings.es_index_mapping_person,
    )
    await es_write_data(
        movie_generator.generate_movies(count=1, movie_id=bulk_query[0].get("_id")),
        test_settings.es_index_movies,
        test_settings.es_index_mapping_film,
    )
    body, headers, status = await http_session_get(
        f"persons/{bulk_query[0].get('_id')}/film"
    )
    assert status == 200
    assert len(body) > 0
