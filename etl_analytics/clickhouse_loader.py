from typing import Any

from clickhouse_driver import Client


class ClickhouseLoader:
    def __init__(self, client: Client) -> None:
        self.__client = client

    def load_data(self, data: Any) -> None:
        ...
    #     self.__client.insert(table_name, data_batch)
    # except Exception as e:
    #     print(f"Error inserting into ClickHouse: {e}")