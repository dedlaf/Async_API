from typing import Any

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    full_name: str
    films: list[dict[str, Any]]
