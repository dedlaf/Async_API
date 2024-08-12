import uuid
from typing import List, Optional

from pydantic import BaseModel, Field


class FakePerson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    films: List[dict] = []


class FakeGenre(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    films: List[dict] = []


class FakeMovie(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    imdb_rating: float
    description: Optional[str] = None
    genres: List[str]
    actors: List[dict]
    actors_names: List[str]
    writers: List[dict]
    writers_names: List[str]
    directors: List[dict]
