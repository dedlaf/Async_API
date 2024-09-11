import uuid
from typing import Optional

from pydantic import BaseModel, Field


class FakePerson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    films: list[dict] = []


class FakeGenre(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    films: list[dict] = []


class FakeMovie(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    imdb_rating: float = 0
    description: Optional[str] = None
    genres: list[str]
    actors: list[dict[str, str]]
    actors_names: list[str]
    writers: list[dict]
    writers_names: list[str]
    directors: list[dict]
