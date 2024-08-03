import os
import sqlite3
from contextlib import contextmanager
from dataclasses import astuple, fields

import psycopg
from my_dataclasses import *


@contextmanager
def conn_context(data_path: str):
    conn = sqlite3.connect(data_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


db_path = "db.sqlite"
dsn = {
    "dbname": "movies_database",
    "user": "app",
    "password": "123qwe",
    "host": "localhost",
    "port": 5432,
    "options": "-c search_path=content",
}


tables = {
    "film_work": Movie(),
    "genre": Genre(),
    "person": Person(),
    "person_film_work": PersonFilmWork(),
    "genre_film_work": GenreFilmWork(),
}


def get_sql_request(data, table):
    row_names = [f.name for f in fields(table[1])]
    all_data = []
    for one_data in data:
        for row_name in row_names:
            if one_data[row_name] is None:
                continue
            else:
                setattr(table[1], row_name, one_data[row_name])
        all_data.append(astuple(table[1]))
    str_row_names = ",".join(row_names)
    col_count = ", ".join(["%s"] * len(row_names))
    sql_request = (
        f"INSERT INTO content.{table[0]} ({str_row_names}) VALUES ({col_count})"
        f"ON CONFLICT (id) DO UPDATE"
        f" SET id = EXCLUDED.id;"
    )
    return sql_request, all_data


def save_all_to_postgres():
    with conn_context(db_path) as conn:
        curs = conn.cursor()
        for i in tables.items():
            curs.execute(f"SELECT * FROM {i[0]};")
            data = ["data"]
            while len(data) != 0:
                data = curs.fetchmany(20)
                fin = get_sql_request(data, i)
                with psycopg.connect(
                    **dsn
                ) as postgres_conn, postgres_conn.cursor() as cursor:
                    cursor.executemany(fin[0], fin[1])


if __name__ == "__main__":
    save_all_to_postgres()
