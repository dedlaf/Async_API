from abc import ABC
from typing import Any

from connection_manager import ConnectionManager
from data_transformer.person_transformer import PersonTransformer
from elasticsearch_loaders.person_elasticsearch_loader import \
    PersonElasticsearchLoader
from postgres_extractors.person_postgres_extractor import \
    PersonPostgresExtractor
from schemas.person import Person
from settings import CHUNK_SIZE
from state import State


class PersonHandler(ABC):
    def __init__(self, state: State, connection_manager: ConnectionManager) -> None:
        self.__state = state

        self.__postgres_extractor = PersonPostgresExtractor(
            CHUNK_SIZE, connection_manager.pg_connection
        )
        self.__data_transformer = PersonTransformer()
        self.__elasticsearch_loader = PersonElasticsearchLoader(
            CHUNK_SIZE, connection_manager.es_client
        )

    def handle_data(self):
        last_modified = self.__state.get_last_modified_person()
        persons_generator = self.__postgres_extractor.extract_data(last_modified)

        for persons in persons_generator:

            if not persons:
                break

            transformed_persons = self.__get_transformed_persons(persons)
            self.__load_persons(transformed_persons)

            self.__set_last_modified_persons(persons)

    def __get_transformed_persons(self, persons: list[dict[str, Any]]) -> list[Person]:
        return self.__data_transformer.transform(persons)

    def __load_persons(self, persons: list[Person]) -> None:
        self.__elasticsearch_loader.load(persons)

    def __set_last_modified_persons(self, persons: list[dict[str, Any]]) -> None:
        last_modified = persons[-1]["modified"]
        self.__state.set_last_modified_person(last_modified)
