from datetime import datetime, timedelta
from typing import Any

from enums import TableName
from postgres_extractors.postgres_extractor import PostgresExtractor
from psycopg2 import DatabaseError


class PersonPostgresExtractor(PostgresExtractor):
    def extract_data(self, last_modified: str) -> Any:
        self.__get_last_modified(last_modified)
        person_ids = self.__get_unique_person_ids()

        return self.__get_persons(person_ids)

    def __get_last_modified(self, last_modified: str) -> None:
        last_modified_dt = datetime.strptime(last_modified, "%Y-%m-%d %H:%M:%S")
        last_modified_dt = last_modified_dt + timedelta(seconds=1)
        self._last_modified = last_modified_dt.strftime("%Y-%m-%d %H:%M:%S")

    def __get_unique_person_ids(self) -> set[str]:
        unique_person_ids = set()

        person_ids_by_role = self.__get_person_id_by_role()
        person_ids = self.__get_person_ids()

        unique_person_ids.update(person_ids_by_role)
        unique_person_ids.update(person_ids)

        return unique_person_ids

    def __get_person_ids(self) -> list[str]:
        self._cursor.execute(
            f"""
        SELECT id, modified
        FROM content.{TableName.PERSON.value}
        WHERE modified > '{self._last_modified}'
        ORDER BY modified """
        )

        return self.__extract_ids()

    def __get_person_id_by_role(self) -> list[str]:
        self._cursor.execute(
            f"""
        SELECT DISTINCT person_id as id, created
        FROM content.{TableName.PERSON_FILM_WORK.value}
        WHERE created > '{self._last_modified}'
        ORDER BY created """
        )

        return self.__extract_ids()

    def __get_persons(self, person_ids: set[str]) -> list[Any]:
        person_ids = list(person_ids)

        query = """
             SELECT
                p.id AS id,
                p.full_name,
                TO_CHAR(p.modified, 'YYYY-MM-DD HH24:MI:SS') AS modified,
                array_agg(DISTINCT jsonb_build_object('id', fw.id, 'roles', film_roles.roles)) AS films
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
            LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
            LEFT JOIN (
                SELECT
                    pfw.person_id,
                    fw.id AS film_work_id,
                    array_agg(pfw.role) AS roles
                FROM content.person_film_work pfw
                JOIN content.film_work fw ON fw.id = pfw.film_work_id
                GROUP BY pfw.person_id, fw.id
            ) film_roles ON film_roles.person_id = p.id AND film_roles.film_work_id = fw.id
            WHERE p.id = ANY(%s::uuid[])
            GROUP BY p.id
            ORDER BY modified;
                """

        self._cursor.execute(query, (person_ids,))

        while rows := self.__extract_data_by_partition():
            yield rows

    def __extract_ids(self) -> list[str]:
        try:
            rows = self._cursor.fetchall()
            return [row["id"] for row in rows]
        except DatabaseError as err:
            raise DatabaseError(f"Произошла ошибка при получении id - {err}")

    def __extract_data_by_partition(self) -> list[Any]:
        try:
            return self._cursor.fetchmany(self._chunk_size)
        except DatabaseError as err:
            raise DatabaseError(f"Произошла ошибка при получении персон - {err}")
