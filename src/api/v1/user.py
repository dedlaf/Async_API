import aiohttp
import uuid
from fastapi import APIRouter

from core.config.components.verify_decorator import verify_user

from schemas.user import UserLoginHistoryResponseSchema

router = APIRouter()


@router.get("/history/{user_id}", response_model=UserLoginHistoryResponseSchema)
@verify_user
async def get_history(user_id: uuid.UUID ) -> UserLoginHistoryResponseSchema:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://nginx:80/auth/history/{user_id}") as response:
            return UserLoginHistoryResponseSchema(response.content.date)
