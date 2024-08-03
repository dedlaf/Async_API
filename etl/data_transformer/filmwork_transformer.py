from typing import Any

from data_transformer.data_transformer import DataTransformer
from schemas.filmwork import Filmwork


class FilmworkTransformer(DataTransformer):
    def transform(self, filmworks: list[Any]) -> list[Filmwork]:
        transformed_filmworks = []

        for filmwork in filmworks:
            directors_names, actors_names, writers_names = self.__get_names(filmwork)
            directors, actors, writers = self.__get_roles(filmwork)

            transformed_filmworks.append(
                Filmwork(
                    id=filmwork.get("id"),
                    imdb_rating=filmwork.get("imdb_rating"),
                    genres=filmwork.get("genres"),
                    title=filmwork.get("title"),
                    description=filmwork.get("description"),
                    directors_names=directors_names,
                    actors_names=actors_names,
                    writers_names=writers_names,
                    directors=directors,
                    actors=actors,
                    writers=writers,
                )
            )

        return transformed_filmworks

    def __get_names(
        self, filmwork: dict[str, Any]
    ) -> tuple[list[str], list[str], list[str]]:
        directors_name = []
        actors_names = []
        writers_names = []

        if people := filmwork.get("people"):
            for person in people:
                if person["role"] == "director":
                    directors_name.append(person["name"])
                elif person["role"] == "actor":
                    actors_names.append(person["name"])
                elif person["role"] == "writer":
                    writers_names.append(person["name"])

        return directors_name, actors_names, writers_names

    def __get_roles(self, filmwork: dict[str, Any]) -> Any:
        directors = []
        actors = []
        writers = []

        if people := filmwork.get("people"):
            for person in people:
                if person["role"] == "director":
                    directors.append({"id": person["id"], "name": person["name"]})
                elif person["role"] == "actor":
                    actors.append({"id": person["id"], "name": person["name"]})
                elif person["role"] == "writer":
                    writers.append({"id": person["id"], "name": person["name"]})

        return directors, actors, writers
