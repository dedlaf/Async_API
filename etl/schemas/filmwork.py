from typing import Any, Optional

from pydantic import BaseModel


class Filmwork(BaseModel):
    id: str
    imdb_rating: Optional[float]
    genres: list[str]
    title: str
    description: Optional[str]
    directors_names: list[str]
    actors_names: list[str]
    writers_names: list[str]
    directors: list[dict[str, Any]]
    actors: list[dict[str, Any]]
    writers: list[dict[str, Any]]
