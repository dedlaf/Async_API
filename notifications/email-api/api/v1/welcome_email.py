import http
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from db.postgres import get_db_connection
from db.redis import get_redis
from schemas.shemas import (ContentCreate, ContentUpdate, EventCreate,
                            TemplateUpdate)
from services.producer_service import Producer, get_producer

router = APIRouter()


@router.post("/")
async def welcome_email(producer: Producer = Depends(get_producer)):
    message = {
        "user_id": "user_id",
        "redirect_uri": "http://localhost:8000/welcome/",
        "timestamp": "86400",
    }
    await producer.publish(message=message, queue_name="welcome_email")
    return {"message": "Welcome email sent"}


@router.get("/{short_id}")
async def redirect_to_long_url(short_id: str, redis: Redis = Depends(get_redis)):
    long_url = await redis.get(short_id)
    if long_url:
        long_url = json.loads(long_url.decode())
        redirect_url = long_url["redirect_uri"]
        return RedirectResponse(url=redirect_url, status_code=301)
    else:
        return None


@router.get("/welcome/")
async def welcome_page():
    return {"message": "Welcome page"}
