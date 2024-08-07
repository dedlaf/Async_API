import uuid
from datetime import datetime
from typing import List, Optional
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from uuid import UUID

from pydantic import BaseModel, Field


class FilmResponse(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str
    imdb_rating: Optional[float] = None


class FilmResponseFull(FilmResponse):
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    genres: List[str]
    actors: List[dict]
    writers: List[dict]
    directors: List[dict]


class GenreResponse(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None


class PersonResponse(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    full_name: str
    films: Optional[List[dict]] = []


def filter_query_string(url, ignoring_args):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filtered_params = {k: v for k, v in query_params.items() if k not in ignoring_args}
    filtered_query = urlencode(filtered_params, doseq=True)
    filtered_url = urlunparse(parsed_url._replace(query=filtered_query))

    return filtered_url


ignoring_request_args = ["page", "page_size"]
