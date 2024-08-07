from datetime import datetime, timedelta
from typing import Any

from enums import TableName
from postgres_extractors.postgres_extractor import PostgresExtractor
from psycopg2 import DatabaseError


class GenrePostgresExtractor(PostgresExtractor):
    def extract_data(self, last_modified: str) -> Any:
        self.__get_last_modified(last_modified)

        return self.__get_genres()

    def __get_last_modified(self, last_modified: str) -> None:
        last_modified_dt = datetime.strptime("2020-05-30 10:05:46", "%Y-%m-%d %H:%M:%S")
        last_modified_dt = last_modified_dt + timedelta(seconds=1)
        self._last_modified = last_modified_dt.strftime("%Y-%m-%d %H:%M:%S")

    def __get_genres(self) -> list[Any]:
        self._cursor.execute(
            f"""
        SELECT id, name, description, TO_CHAR(modified, 'YYYY-MM-DD HH24:MI:SS') as modified
        FROM content.{TableName.GENRE.value}
        WHERE modified > '{self._last_modified}'
        ORDER BY modified """
        )

        return self.__extract_genres()

    def __extract_genres(self) -> list[str]:
        try:
            return self._cursor.fetchall()
        except DatabaseError as err:
            raise DatabaseError(f"Произошла ошибка при получении жанров - {err}")
