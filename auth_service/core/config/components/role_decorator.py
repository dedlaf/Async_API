import jwt
from functools import wraps

from fastapi import HTTPException, Request, status, Depends

from db.redis import get_redis
from db.session import get_db_function
from hash import hash_data
from services.role_service import RoleService
from services.user_service import UserService


def has_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        redis = await get_redis()
        user_service = UserService(get_db_function())
        role_service = RoleService(get_db_function())
        access_token = request.cookies.get('access_token_cookie')

        # TODO refresh token
        try:
            decode_token = jwt.decode(access_token, "secret", algorithms=["HS256"])
        except :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        if not decode_token.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        username = decode_token['sub']
        user_agent = request.headers.get("user-agent")
        byte_agent = bytes(user_agent, encoding="utf-8")
        storage_token = await redis.get(f"access_token:{username}:{hash_data(byte_agent)}")

        if not storage_token or (storage_token.decode() != str(access_token)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized"
            )

        user = user_service.get_user_by_username(username)
        role = role_service.get_role_by_name('admin')

        if not(user and role and user_service.has_role(user, role)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Method not found"
            )

        return await func(*args, **kwargs)

    return wrapper
