import time

import backoff
import psycopg2
from config import (backoff_configs, backoff_configs_for_postgres, dsn, es,
                    final_data, list_of_film, list_of_persons, logger,
                    redis_connection, redis_storage, sql_requests)
from elasticsearch import Elasticsearch
from get_lists_for_redis import (get_list_of_films, get_list_of_films_id,
                                 get_list_of_persons)

"""Function to load data from redis to Elastic"""


@backoff.on_exception(**backoff_configs)
def redis_to_els(keys: list) -> None:
    for key in keys:
        value = redis_storage.retrieve_state(key)
        try:
            doc = {
                "id": value["film_id"],
                "title": value["title"],
                "description": value["description"],
                "imdb_rating": value["rating"],
                "actors": value["persons"],
                "genres": value["genres"],
            }
            es.index(index="movies", id=value["film_id"], body=doc)
        except Exception as e:
            logger.exception(e)


@backoff.on_exception(**backoff_configs_for_postgres)
def postgres_to_redis() -> None:
    with psycopg2.connect(**dsn) as postgres_conn, postgres_conn.cursor() as cursor:
        cursor.execute(sql_requests[0])
        get_list_of_persons(list_of_persons, cursor)
        cursor.execute(
            sql_requests[1].replace("'id'", redis_storage.retrieve_state("persons"))
        )
        get_list_of_films_id(list_of_film, cursor)
        cursor.execute(
            sql_requests[2].replace(
                "'films_id'", redis_storage.retrieve_state("films_id")
            )
        )
        get_list_of_films(final_data, cursor)
        cursor.close()


if __name__ == "__main__":
    while True:
        time.sleep(10)
        postgres_to_redis()
        try:
            keys = redis_connection.keys("*")
            redis_to_els(keys)
        except elasticsearch.ConnectionError:
            logger.exception("Elasticsearch connection error")
            time.sleep(10)
        logger.info("Sleeping for 60 seconds, then continue to detect data")
