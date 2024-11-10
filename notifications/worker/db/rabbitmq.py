from typing import Optional

from aio_pika.robust_connection import RobustConnection

rabbitmq: Optional[RobustConnection] = None


async def get_rabbitmq() -> RobustConnection:
    return rabbitmq
