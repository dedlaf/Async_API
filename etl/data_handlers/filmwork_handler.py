from abc import ABC
from typing import Any

from connection_manager import ConnectionManager
from data_transformer.filmwork_transformer import FilmworkTransformer
from elasticsearch_loaders.filmwork_elasticsearch_loader import (
    FilmworkElasticsearchLoader,
)
from postgres_extractors.filmwork_postgres_extractor import FilmworkPostgresExtractor
from schemas.filmwork import Filmwork
from settings import CHUNK_SIZE
from state import State


class FilmworkHandler(ABC):
    def __init__(self, state: State, connection_manager: ConnectionManager) -> None:
        self.__state = state

        self.__postgres_extractor = FilmworkPostgresExtractor(
            CHUNK_SIZE, connection_manager.pg_connection
        )
        self.__data_transformer = FilmworkTransformer()
        self.__elasticsearch_loader = FilmworkElasticsearchLoader(
            CHUNK_SIZE, connection_manager.es_client
        )

    def handle_data(self):
        last_modified = self.__state.get_last_modified_filmwork()
        filmworks_generator = self.__postgres_extractor.extract_data(last_modified)

        for filmworks in filmworks_generator:

            if not filmworks:
                break

            transformed_filmworks = self.__get_transformed_filmworks(filmworks)
            self.__load_data(transformed_filmworks)

            self.__set_last_modified_filmwork(filmworks)

    def __get_transformed_filmworks(
        self, filmworks: list[dict[str, Any]]
    ) -> list[Filmwork]:
        return self.__data_transformer.transform(filmworks)

    def __load_data(self, filmworks: list[Filmwork]) -> None:
        self.__elasticsearch_loader.load(filmworks)

    def __set_last_modified_filmwork(self, filmworks: list[dict[str, Any]]) -> None:
        last_modified = filmworks[-1]["modified"]
        self.__state.set_last_modified_filmwork(last_modified)
