from typing import Dict

from beanie import Document


class Like(Document):
    movie_id: str
    user_ratings: Dict[str, int]  # словарь с user_id и их оценками
    rating: float = 0.0  # средняя оценка фильма, по умолчанию 0.0
