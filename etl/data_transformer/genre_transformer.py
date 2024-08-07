from typing import Any
import logging
from data_transformer.data_transformer import DataTransformer
from schemas.genre import Genre


class GenreTransformer(DataTransformer):
    def transform(self, genres: list[Any]) -> list[Genre]:
        transformed_genres = []

        for genre in genres:
            transformed_genres.append(
                Genre(
                    id=genre["id"], name=genre["name"], description=genre["description"]
                )
            )
        logging.info(transformed_genres)
        return transformed_genres
