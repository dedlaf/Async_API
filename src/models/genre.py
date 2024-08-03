from typing import Optional

from models.mixin import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    name: str
    description: Optional[str] = None
