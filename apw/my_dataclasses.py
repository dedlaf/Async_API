import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass()
class Movie:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default="")
    description: str = field(default="")
    creation_date: datetime.date = field(default=datetime.now(timezone.utc))
    rating: float = field(default=0.0)
    type: str = field(default="movie")
    created_at: datetime = field(default=datetime.now(timezone.utc))
    updated_at: datetime = field(default=datetime.now(timezone.utc))


@dataclass()
class Person:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = field
    created_at: datetime = field(default=datetime.now(timezone.utc))
    updated_at: datetime = field(default=datetime.now(timezone.utc))


@dataclass()
class PersonFilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default="")
    created_at: datetime = field(default=datetime.now(timezone.utc))


@dataclass()
class Genre:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default="")
    description: str = field(default="")
    created_at: datetime = field(default=datetime.now(timezone.utc))
    updated_at: datetime = field(default=datetime.now(timezone.utc))

    def __post_init__(self):
        if self.description is None:
            self.description = ""


@dataclass()
class GenreFilmWork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now(timezone.utc))
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
