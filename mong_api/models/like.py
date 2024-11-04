from typing import Dict

from beanie import Document


class Like(Document):
    movie_id: str
    user_ratings: Dict[str, int]  # словарь с user_id и их оценками
    rating: float = 0.0  # средняя оценка фильма, по умолчанию 0.0

    async def insert(self, *args, **kwargs):
        self._update_rating()
        await super().insert(*args, **kwargs)

    async def save(self, *args, **kwargs):
        self._update_rating()
        await super().save(*args, **kwargs)

    def _update_rating(self):
        if self.user_ratings:
            total_ratings = sum(self.user_ratings.values())
            count = len(self.user_ratings)
            self.rating = round(max(0, min(total_ratings / count, 10)), 1)
