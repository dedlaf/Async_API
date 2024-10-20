from kafka.consumer.fetcher import ConsumerRecord

from schemas import Message


class DataTransformer:
    def transform_data(self, message: ConsumerRecord) -> Message:
        return Message(
            topic=message.topic,
            key=message.key.decode("utf-8"),
            value=message.value.decode("utf-8"),
        )
