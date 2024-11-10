import json

import aio_pika
from aio_pika.robust_channel import RobustChannel
from aio_pika.robust_connection import RobustConnection
from aio_pika.robust_queue import RobustQueue
from fastapi import Depends

from db.rabbitmq import get_rabbitmq


class Producer:
    def __init__(self, rabbitmq: RobustConnection):
        self.__connection = rabbitmq

    async def publish(self, message: dict, queue_name: str):
        channel: RobustChannel = await self.__connection.channel()
        queue: RobustQueue = await channel.declare_queue(queue_name, durable=True)
        json_str = json.dumps(message)
        rabbitmq_body = json_str.encode("utf-8")
        await channel.default_exchange.publish(
            message=aio_pika.Message(body=rabbitmq_body), routing_key=queue.name
        )


def get_producer(rabbitmq=Depends(get_rabbitmq)):
    return Producer(rabbitmq=rabbitmq)
