from kafka import KafkaConsumer


class KafkaExtractor:
    def __init__(self, connection: KafkaConsumer) -> None:
        self.__connection = connection

    def extract_messages(self) -> dict:
        return self.__connection.poll(timeout_ms=5000)

    def commit_message(self) -> None:
        self.__connection.commit()
