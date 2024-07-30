from typing import Optional

from src.models.mixin import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    name: str
    description: Optional[str] = None
