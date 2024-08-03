from datetime import datetime
from typing import Optional

from models.mixin import TimeStampedMixin, UUIDMixin


class Film(TimeStampedMixin, UUIDMixin):
    title: str
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    imdb_rating: Optional[float] = None
    genres: list
