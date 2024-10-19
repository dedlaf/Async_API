from kafka import KafkaConsumer


class KafkaExtractor:
    def __init__(self, connection: KafkaConsumer) -> None:
        self.__connection = connection

    def extract_messages(self):
        return self.__connection
