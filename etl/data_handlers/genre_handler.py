from abc import ABC
from typing import Any

from connection_manager import ConnectionManager
from data_transformer.genre_transformer import GenreTransformer
from elasticsearch_loaders.genre_elasticsearch_loader import GenreElasticsearchLoader
from postgres_extractors.genre_postgres_extractor import GenrePostgresExtractor
from schemas.genre import Genre
from settings import CHUNK_SIZE
from state import State


class GenreHandler(ABC):
    def __init__(self, state: State, connection_manager: ConnectionManager) -> None:
        self.__state = state

        self.__postgres_extractor = GenrePostgresExtractor(
            CHUNK_SIZE, connection_manager.pg_connection
        )
        self.__data_transformer = GenreTransformer()
        self.__elasticsearch_loader = GenreElasticsearchLoader(
            CHUNK_SIZE, connection_manager.es_client
        )

    def handle_data(self):
        last_modified = self.__state.get_last_modified_genre()
        genres = self.__postgres_extractor.extract_data(last_modified)

        if genres:
            transformed_genres = self.__get_transformed_genres(genres)
            self.__load_genres(transformed_genres)

            self.__set_last_modified_genre(genres)

    def __get_transformed_genres(self, genres: list[dict[str, Any]]) -> list[Genre]:
        return self.__data_transformer.transform(genres)

    def __load_genres(self, genres: list[Genre]) -> None:
        self.__elasticsearch_loader.load(genres)

    def __set_last_modified_genre(self, genres: list[dict[str, Any]]) -> None:
        last_modified = genres[-1]["modified"]
        self.__state.set_last_modified_genre(last_modified)
