import pika
import psycopg2
from settings import config
import backoff


@backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_tries=5)
def get_db_connection():
    return psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_username,
        password=config.db_password,
        database=config.db_database,
    )


@backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_tries=5)
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        config.rabbitmq_default_user, config.rabbitmq_default_pass
    )
    parameters = pika.ConnectionParameters(
        config.rabbitmq_host, config.rabbitmq_port, "/", credentials
    )
    return pika.BlockingConnection(parameters)


