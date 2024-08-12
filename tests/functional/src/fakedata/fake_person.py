from faker import Faker
import uuid
from .base_models import FakePerson
from ...settings import test_settings


class FakePersonData:
    def __init__(self):
        self.fake = Faker()

    def generate_person(self, movie_id=None):
        person = FakePerson(full_name=self.fake.name())
        if movie_id is None:
            movie_id = str(uuid.uuid4())
        person.films.append({"id": movie_id, "roles": [self.fake.word()]})
        return self._transform_to_es(person=person)

    def generate_people(self, count=10, movie_id=None):
        return [self.generate_person(movie_id) for _ in range(count)]

    @staticmethod
    def _transform_to_es(person):
        return {
                '_id': person.id,
                '_index': test_settings.es_index_persons,
                '_source': {
                    'id': person.id,
                    'full_name': person.full_name,
                    'films': person.films,
                    }
                }
