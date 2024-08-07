from typing import Any

from data_transformer.data_transformer import DataTransformer
from schemas.person import Person


class PersonTransformer(DataTransformer):
    def transform(self, persons: list[Any]) -> list[Person]:
        transformed_persons = []

        for person in persons:
            transformed_persons.append(
                Person(
                    id=person["id"],
                    full_name=person["full_name"],
                    films=person["films"],
                )
            )

        return transformed_persons
