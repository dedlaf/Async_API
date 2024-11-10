import json
import pika


class Producer:
    def __init__(self, rabbitmq):
        self.__connection = rabbitmq
        self.__channel = self.__connection.channel()

    def publish(self, message: dict, queue_name: str):
        self.__channel.queue_declare(queue=queue_name, durable=True)
        json_str = json.dumps(message)
        rabbitmq_body = json_str.encode("utf-8")
        self.__channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=rabbitmq_body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )

    def close(self):
        self.__connection.close()
