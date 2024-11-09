from aio_pika import connect_robust
from consumer import Consumer
import asyncio
from email_sender import email_sender

async def main():
    rabbitmq = await connect_robust(
        host='localhost',
        login='dedlaf',
        password='123qwe',
        port=5672,
    )


    consumer = Consumer(rabbitmq)
    await consumer.get_messages('welcome_email', 'delayed_notify')
    await consumer.get_template()
    await consumer.get_email("39e73776-5f57-4f91-99af-3290ec47c2ba")
    try:
        await asyncio.Future()
    finally:
        await rabbitmq.close()
        email_sender.disconnect()



loop = asyncio.get_event_loop()
loop.run_until_complete(main())

