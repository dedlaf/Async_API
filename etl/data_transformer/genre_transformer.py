from typing import Any

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

        return transformed_genres
