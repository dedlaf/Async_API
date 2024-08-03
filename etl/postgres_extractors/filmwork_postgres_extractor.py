from datetime import datetime, timedelta
from typing import Any

from enums import TableName
from postgres_extractors.postgres_extractor import PostgresExtractor
from psycopg2 import DatabaseError


class FilmworkPostgresExtractor(PostgresExtractor):
    def extract_data(self, last_modified: str) -> Any:
        self.__get_last_modified(last_modified)
        filmwork_ids = self.__get_unique_filmwork_ids()

        return self.__get_filmworks(filmwork_ids)

    def __get_last_modified(self, last_modified: str) -> None:
        last_modified_dt = datetime.strptime(last_modified, "%Y-%m-%d %H:%M:%S")
        last_modified_dt = last_modified_dt + timedelta(seconds=1)
        self._last_modified = last_modified_dt.strftime("%Y-%m-%d %H:%M:%S")

    def __get_unique_filmwork_ids(self) -> set[str]:
        unique_filmwork_ids = set()

        person_ids = self.__get_person_ids()
        genre_ids = self.__get_genre_ids()

        filmwork_ids = self.__get_filmwork_ids()
        filmwork_ids_by_person = self.__get_filmwork_ids_by_person(person_ids)
        filmwork_ids_by_genre = self.__get_filmwork_ids_by_genre(genre_ids)

        unique_filmwork_ids.update(filmwork_ids)
        unique_filmwork_ids.update(filmwork_ids_by_person)
        unique_filmwork_ids.update(filmwork_ids_by_genre)

        return unique_filmwork_ids

    def __get_person_ids(self) -> list[str]:
        return self.__get_ids(TableName.PERSON.value)

    def __get_genre_ids(self) -> list[str]:
        return self.__get_ids(TableName.GENRE.value)

    def __get_filmwork_ids(self) -> list[str]:
        return self.__get_ids(TableName.FILM_WORK.value)

    def __get_ids(self, table_name: str) -> list[str]:
        self._cursor.execute(
            f"""
        SELECT id, modified
        FROM content.{table_name}
        WHERE modified > '{self._last_modified}'
        ORDER BY modified """
        )

        return self.__extract_ids()

    def __get_filmwork_ids_by_person(self, person_ids: list[str]) -> list[str]:
        query = """
        SELECT fw.id
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        WHERE pfw.person_id = ANY(%s::uuid[])
        ORDER BY fw.modified
        """

        self._cursor.execute(query, (person_ids,))

        return self.__extract_ids()

    def __get_filmwork_ids_by_genre(self, genre_ids: list[str]) -> list[str]:
        query = """
        SELECT fw.id
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        WHERE gfw.genre_id = ANY(%s::uuid[])
        ORDER BY fw.modified
        """

        self._cursor.execute(query, (genre_ids,))

        return self.__extract_ids()

    def __get_filmworks(self, filmwork_ids: set[str]) -> Any:
        filmwork_ids = list(filmwork_ids)

        query = """
        SELECT
            fw.id as id,
            fw.title,
            fw.description,
            fw.rating as imdb_rating,
            fw.type,
            TO_CHAR(fw.modified, 'YYYY-MM-DD HH24:MI:SS') as modified,
            array_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name, 'role', pfw.role)) as people,
            array_agg(DISTINCT g.name) as genres
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.id = ANY(%s::uuid[])
        GROUP BY fw.id
        ORDER BY modified
        """

        self._cursor.execute(query, (filmwork_ids,))

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
            raise DatabaseError(f"Произошла ошибка при получении фильмов - {err}")
