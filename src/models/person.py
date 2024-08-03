from models.mixin import TimeStampedMixin, UUIDMixin


class Person(TimeStampedMixin, UUIDMixin):
    full_name: str
