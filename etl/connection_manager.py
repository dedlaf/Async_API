from typing import Any

import backoff
import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from settings import DSL, ELASTIC_HOST


class ConnectionManager:
    def __init__(self) -> None:
        self.__pg_connection = None
        self.__es_client = None

    @property
    def pg_connection(self) -> _connection:
        if self.__pg_connection is None:
            self.__pg_connection = self.__get_pg_connection()
        return self.__pg_connection

    @property
    def es_client(self) -> Any:
        if self.__es_client is None:
            self.__es_client = self.__get_es_client()
        return self.__es_client

    @backoff.on_exception(
        backoff.expo, psycopg2.OperationalError, factor=2, max_time=600
    )
    def __get_pg_connection(self) -> _connection:
        conn = psycopg2.connect(**DSL, cursor_factory=RealDictCursor)

        return conn

    @backoff.on_exception(backoff.expo, ConnectionError, factor=2, max_time=600)
    def __get_es_client(self) -> Any:
        es_client = Elasticsearch([ELASTIC_HOST])

        if not es_client.ping():
            raise ConnectionError

        return es_client
