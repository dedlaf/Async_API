from datetime import datetime
from typing import Optional

from models.mixin import TimeStampedMixin, UUIDMixin


class Film(TimeStampedMixin, UUIDMixin):
    title: str
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    rating: Optional[float] = None
    type: str
