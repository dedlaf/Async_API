import json
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
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=[settings.bootstrap_servers],
                auto_offset_reset="latest",
                #enable_auto_commit=True,
                group_id="etl_kafka_clickhouse",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )

            available_topics = list(consumer.topics())

            consumer.subscribe(available_topics)

            return consumer
        except Exception as e:
            raise

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def __get_clickhouse_connection(self) -> Client:
        try:
            clickhouse_client = Client(host="localhost:8213")
            return clickhouse_client
        except Exception as e:
            raise
