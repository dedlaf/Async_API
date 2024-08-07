from typing import List, Optional

from models.mixin import TimeStampedMixin, UUIDMixin


class Person(TimeStampedMixin, UUIDMixin):
    full_name: str
    films: Optional[List[dict]] = []
