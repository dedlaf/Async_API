import asyncio
import logging

import backoff
from aio_pika import connect_robust
from aiormq import AMQPConnectionError

from consumer import Consumer
from email_sender import email_sender
from settings import settings


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@backoff.on_exception(backoff.expo, AMQPConnectionError)
async def main():
    rabbitmq = await connect_robust(
        host=settings.rabbitmq_host,
        login=settings.rabbitmq_default_user,
        password=settings.rabbitmq_default_pass,
        port=settings.rabbitmq_port,
    )

    consumer = Consumer(rabbitmq)
    await consumer.get_messages("welcome_email", "delayed_notify")
    try:
        await asyncio.Future()
    finally:
        await rabbitmq.close()
        email_sender.disconnect()


logging.info("Start")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
