from fastapi import APIRouter, Depends
from services.producer_service import get_producer, Producer
from db.redis import get_redis
from redis.asyncio import Redis
import json
from starlette.responses import RedirectResponse

router = APIRouter()


@router.post('/')
async def welcome_email(producer: Producer = Depends(get_producer)):
    message = {"user_id": "user_id", "redirect_uri": "http://localhost:8000/welcome/", "timestamp": "86400"}
    await producer.publish(message=message, queue_name='welcome_email')
    return {'message': 'Welcome email sent'}


@router.get('/{short_id}')
async def redirect_to_long_url(short_id: str, redis: Redis = Depends(get_redis)):
    long_url = await redis.get(short_id)
    if long_url:
        long_url = json.loads(long_url.decode())
        redirect_url = long_url['redirect_uri']
        return RedirectResponse(url=redirect_url, status_code=301)
    else:
        return None


@router.get('/welcome/')
async def welcome_page():
    return {'message': 'Welcome page'}
