from clickhouse_loader import ClickhouseLoader
from data_transformer import DataTransformer
from etl_analytics_connection_manager import ETLAnalyticsConnectionManager
from kafka_extractor import KafkaExtractor


class ETLAnalyticsProcessHandler:
    def __init__(self) -> None:
        connection_manager = ETLAnalyticsConnectionManager()

        self.__kafka_extractor = KafkaExtractor(connection_manager.kafka_connection)
        self.__data_transformer = DataTransformer()
        self.__clickhouse_loader = ClickhouseLoader(
            connection_manager.clickhouse_connection
        )

    def handle_process(self) -> None:
        messages = self.__kafka_extractor.extract_messages()

        for message in messages:
            transformed_data = self.__data_transformer.transform_data(message)

            self.__clickhouse_loader.load_data(transformed_data)