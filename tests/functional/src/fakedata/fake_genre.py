from faker import Faker

from .base_models import FakeGenre


class FakeGenreData:
    def __init__(self) -> None:
        self.fake = Faker()

    def generate_genre(self, movie_id: str = None) -> FakeGenre:
        genre = FakeGenre(name=self.fake.word(), description="")

        if movie_id:
            genre.films.append({"id": movie_id})
        return genre

    def generate_genres(self, count: int = 10, movie_id: str = None) -> list[FakeGenre]:
        return [self.generate_genre(movie_id) for _ in range(count)]

    @staticmethod
    def transform_to_es(genres: list[FakeGenre]) -> list[dict]:
        return [
            {
                "_id": genre.id,
                "_index": "genres",
                "_source": {
                    "id": genre.id,
                    "name": genre.name,
                    "description": genre.description,
                },
            }
            for genre in genres
        ]
