import json
import logging
from datetime import datetime

import aio_pika
import requests
from email_sender import email_sender
from redis.asyncio import Redis
from short_url import URLShortener

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Consumer:
    def __init__(self, rabbitmq: aio_pika.RobustConnection):
        self.short_url = URLShortener(
            redis_client=Redis(host="localhost", port=6379, db=0)
        )
        self.__connection = rabbitmq

    async def get_messages(self, queue_name: str, queue_name1: str):
        channel = await self.__connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue1 = await channel.declare_queue(queue_name, durable=True)
        queue2 = await channel.declare_queue(queue_name1, durable=True)
        await queue1.consume(self._welcome_message)
        await queue2.consume(self._delayed_notify)
        logging.info("Started consuming")

    async def _welcome_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            body = message.body.decode()
            short_url = await self.get_short(body[0])
            context = {
                "redirect_uri": short_url,
                "company_name": "Online-cinema",
                "year": datetime.now().year,
            }
            user_id = body["user_id"]
            email = self.get_email(user_id)
            body = email_sender.render_template_from_file("welcome_email.html", context)
            email_sender.send_email(
                to_email=email, subject="Welcome", body=body
            )

    async def _delayed_notify(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            content = data["content"]
            template = data["template"]
            body = email_sender.render_template(template, content)
            users = data["users"].split(",")
            emails = [await self.get_email(user) for user in users]
            for email in emails:
                email_sender.send_email(to_email=email, subject="Welcome", body=body)

    async def get_short(self, message):
        return await self.short_url.encode_url(long_url=message)

    @staticmethod
    async def get_template(path="templates/welcome_email.html"):
        template = requests.get("http://localhost/media/" + path)
        return template.content.decode()

    @staticmethod
    async def get_email(user_id):
        response = requests.get(f"http://auth:8070/auth/user/{user_id}")
        email = json.loads(response.content.decode())["email"]
        return email
