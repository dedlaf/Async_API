import json

from pydantic import Field
from pydantic_settings import BaseSettings

with open("es_mappings/movies_mapping.json", "r") as file:
    movies_json = file.read()
    movies = json.loads(movies_json)

with open("es_mappings/persons_mapping.json", "r") as file:
    person_json = file.read()
    persons = json.loads(person_json)

with open("es_mappings/genres_mapping.json", "r") as file:
    genre_json = file.read()
    genres = json.loads(genre_json)


class TestSettings(BaseSettings):
    es_host: str = Field(
        "http://elasticsearch:9200", json_schema_extra={"env": "ELASTIC_HOST"}
    )
    es_index_movies: str = Field("movies")
    es_index_persons: str = Field("persons")
    es_index_genres: str = Field("genres")

    es_index_mapping_film: dict = Field(movies)
    es_index_mapping_person: dict = Field(persons)
    es_index_mapping_genres: dict = Field(genres)

    es_page_size: int = 50

    redis_host: str = Field(
        "http://redis:6379", json_schema_extra={"env": "REDIS_HOST"}
    )
    service_url: str = Field("http://nginx")


test_settings = TestSettings()
