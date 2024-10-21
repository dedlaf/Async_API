import backoff
from clickhouse_driver import Client

from schemas import Message


class ClickhouseLoader:
    def __init__(self, client: Client) -> None:
        self.__client = client

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def load_data(self, messages: list[Message], topic: str) -> None:
        if not self.__is_table_exists(topic):
            self.__create_table(topic)

        self.__insert_message(messages, topic)

    def __create_table(self, topic: str) -> None:
        table_name = f"topic_{topic}"

        create_table_query = f"""
        CREATE TABLE {table_name} (
            key String,
            value String
        ) ENGINE = MergeTree()
        ORDER BY key
        """
        self.__client.execute(create_table_query)

    def __is_table_exists(self, topic: str) -> bool:
        table_name = f"topic_{topic}"
        query = f"SELECT count() FROM system.tables WHERE name = '{table_name}' AND database = 'default'"
        result = self.__client.execute(query)

        return result[0][0] > 0

    def __insert_message(self, messages: list[Message], topic: str) -> None:
        table_name = f"topic_{topic}"

        insert_query = f"INSERT INTO {table_name} (key, value) VALUES"
        self.__client.execute(insert_query, [(message.key, message.value) for message in messages])
