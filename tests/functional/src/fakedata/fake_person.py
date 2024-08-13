from faker import Faker
import uuid
import sys
sys.path.append("..")
from .base_models import FakePerson
from ..settings import test_settings


class FakePersonData:
    def __init__(self) -> None:
        self.fake = Faker()

    def generate_person(self, movie_id: str = None) -> FakePerson:
        person = FakePerson(full_name=self.fake.name())
        if movie_id is None:
            movie_id = str(uuid.uuid4())
        person.films.append({"id": movie_id, "roles": [self.fake.word()]})
        return person

    def generate_people(self, count: int = 10, movie_id: str = None) -> list[FakePerson]:
        return [self.generate_person(movie_id) for _ in range(count)]

    @staticmethod
    def transform_to_es(persons: list[FakePerson]) -> list[dict]:
        return [{
                '_id': person.id,
                '_index': test_settings.es_index_persons,
                '_source': {
                    'id': person.id,
                    'full_name': person.full_name,
                    'films': person.films,
                    }
                } for person in persons]
