from typing import List

from beanie import Document


class User(Document):
    name: str
    email: str
    age: int
    bookmarks: List[str] = []
