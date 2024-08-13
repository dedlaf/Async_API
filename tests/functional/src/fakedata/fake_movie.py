import uuid

from faker import Faker
import sys
sys.path.append("..")
from .base_models import FakeMovie
from ..settings import test_settings


class FakeMovieData:
    def __init__(self, person_generator, genre_generator):
        self.fake = Faker()
        self.person_generator = person_generator
        self.genre_generator = genre_generator

    def _generate_persons(self, movie_id):
        actors = self.person_generator.generate_people(2, movie_id)
        writers = self.person_generator.generate_people(2, movie_id)
        directors = self.person_generator.generate_people(1, movie_id)
        return actors, writers, directors

    def _generate_genres(self, movie_id):
        return self.genre_generator.generate_genres(2, movie_id)

    def _generate_movie_data(self, movie_id, bundle=False):
        if movie_id is None:
            movie_id = str(uuid.uuid4())
        actors, writers, directors = self._generate_persons(movie_id)
        genres = self._generate_genres(movie_id)
        movie = FakeMovie(
            id=movie_id,
            imdb_rating=round(self.fake.random.uniform(1, 10), 1),
            genres=[genre.name for genre in genres],
            title=self.fake.sentence(nb_words=3, variable_nb_words=False),
            description=self.fake.text(max_nb_chars=10),
            actors=[{"id": actor.id, "name": actor.full_name} for actor in actors],
            actors_names=[actor.full_name for actor in actors],
            writers=[
                {"id": writer.id, "name": writer.full_name} for writer in writers
            ],
            writers_names=[writer.full_name for writer in writers],
            directors=[
                {"id": director.id, "name": director.full_name}
                for director in directors
            ],
            directors_names=[director.full_name for director in directors]
        )
        if bundle:
            return {
                'movies': movie,
                'genres': genres,
                'persons': [*actors, *writers, *directors]
            }

        return movie

    def generate_movie(self, movie_id=None, bundle=False):
        return self._generate_movie_data(movie_id, bundle)

    def generate_movies(self, count=10, movie_id=None, bundle=False):
        return [self.generate_movie(movie_id, bundle) for _ in range(count)]

    @staticmethod
    def transform_to_es(movies):
        return [{
            "_id": movie.id,
            "_index": test_settings.es_index_movies,
            "_source": movie.model_dump()
        } for movie in movies]
