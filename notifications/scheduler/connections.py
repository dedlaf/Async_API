import psycopg2
from settings import config
import pika


def get_db_connection():
    return psycopg2.connect(
        host="db",
        port="5432",
        user="app",
        password="123qwe",
        database="movies_database"
    )


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(config.rabbitmq_default_user, config.rabbitmq_default_pass)
    parameters = pika.ConnectionParameters(config.rabbitmq_host, config.rabbitmq_port, '/', credentials)
    return pika.BlockingConnection(parameters)
