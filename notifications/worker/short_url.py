import random
import string


class URLShortener:
    def __init__(self, redis_client, ttl=86400):
        self.redis = redis_client
        self.ttl = ttl

    @staticmethod
    def _generate_short_id(length=6):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    async def encode_url(self, long_url):
        short_id = self._generate_short_id()
        while await self.redis.exists(short_id):
            short_id = self._generate_short_id()

        await self.redis.setex(short_id, self.ttl, long_url)
        return f"http://localhost:8000/{short_id}"

    def decode_url(self, short_id):
        long_url = self.redis.get(short_id)
        if long_url:
            return long_url.decode()
        else:
            return None
