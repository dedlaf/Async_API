from typing import Any

import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer
from settings import Settings

settings = Settings()


class ETLAnalyticsConnectionManager:
    def __init__(self) -> None:
        self.__kafka_connection = None
        self.__clickhouse_connection = None

    @property
    def kafka_connection(self) -> KafkaConsumer:
        if self.__kafka_connection is None:
            self.__kafka_connection = self.__get_kafka_connection()

        return self.__kafka_connection

    @property
    def clickhouse_connection(self) -> Any:
        if self.__clickhouse_connection is None:
            self.__clickhouse_connection = self.__get_clickhouse_connection()

        return self.__clickhouse_connection

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def __get_kafka_connection(self) -> KafkaConsumer:
        consumer = KafkaConsumer(
            bootstrap_servers=[settings.bootstrap_servers],
            group_id="etl",
        )

        available_topics = list(consumer.topics())

        consumer.subscribe(available_topics)

        return consumer

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def __get_clickhouse_connection(self) -> Client:
        clickhouse_client = Client(host=settings.clickhouse_host)
        return clickhouse_client
