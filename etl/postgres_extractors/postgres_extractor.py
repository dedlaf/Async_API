from abc import abstractmethod
from typing import Any

from psycopg2.extensions import connection as _connection


class PostgresExtractor:
    def __init__(self, chunk_size: int, connection: _connection) -> None:
        self._cursor = connection.cursor()
        self._chunk_size = chunk_size

        self._last_modified = ""

    @abstractmethod
    def extract_data(self, last_modified: str) -> Any: ...
