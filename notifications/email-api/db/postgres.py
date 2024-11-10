import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host="db",
        port="5432",
        user="app",
        password="123qwe",
        database="movies_database"
    )
