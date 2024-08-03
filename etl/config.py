import json
import logging
import os

import backoff
import elasticsearch
import psycopg2
import redis
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


"""Configs for Redis"""


class BaseStorage:
    def save_state(self, state: dict[str, any], key: str) -> None:
        pass

    def retrieve_state(self, key: str) -> dict[str, any]:
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis: redis.Redis) -> None:
        self._redis = redis

    def save_state(self, state: dict[str, any], key: str) -> None:
        serialized_state = json.dumps(state, default=str)
        self._redis.set(key, serialized_state)

    def retrieve_state(self, key: str) -> dict[str, any]:
        serialized_state = self._redis.get(key)
        if serialized_state:
            return json.loads(serialized_state)
        return {}


redis_connection = redis.Redis(
    host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT")
)
redis_storage = RedisStorage(redis_connection)


"""Configs for db"""
dsn = {
    "dbname": os.environ.get("DSN_NAME"),
    "user": os.environ.get("DSN_USER"),
    "password": os.environ.get("DSN_PASSWORD"),
    "host": os.environ.get("DSN_HOST"),
    "port": os.environ.get("DSN_PORT"),
    "options": os.environ.get("DSN_OPTIONS"),
}


"""Postgres requests to get data"""
sql_requests = [
    f"SELECT id, updated_at FROM content.person WHERE updated_at > '1900-06-16 20:14:09.313086+00'"
    f" ORDER BY updated_at;",
    f"SELECT fw.id, fw.updated_at, fw.title FROM content.film_work fw LEFT JOIN content.person_film_work pfw"
    f" ON pfw.film_work_id = fw.id WHERE pfw.person_id IN ('id') ORDER BY fw.updated_at;",
    f"SELECT fw.id as fw_id, fw.title, fw.description, fw.rating, fw.type,"
    f" fw.created_at, fw.updated_at, pfw.role, p.id, p.full_name, g.name FROM content.film_work fw"
    f" LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id LEFT JOIN content.person p"
    f" ON p.id = pfw.person_id LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id "
    f"LEFT JOIN content.genre g ON g.id = gfw.genre_id WHERE fw.id IN ('films_id');",
]

"""Variables"""
list_of_persons = []
list_of_film = []
final_data = []
batch_size = 100

logging.info(os.environ.get("ES_HOSTS"))
"""Elasticsearch connection"""
es = Elasticsearch("http://elasticsearch:9200")
"""Configs for logger"""
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger("elasticsearch")

"""Configs for backoff"""
backoff_configs = {
    "wait_gen": backoff.expo,
    "exception": (requests.exceptions.RequestException, elasticsearch.ConnectionError),
    "logger": logger,
    "max_tries": 100,
}

backoff_configs_for_postgres = {
    "wait_gen": backoff.expo,
    "exception": (psycopg2.InterfaceError, psycopg2.OperationalError),
    "logger": logger,
    "max_tries": 100,
}
