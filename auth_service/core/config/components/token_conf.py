from datetime import timedelta

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import Depends


class Tokens:
    def __init__(self, auth: AuthJWT):
        self.auth = auth

    async def validate(self):
        await self.auth.jwt_required()
        return await self.auth.get_jwt_subject()

    async def create(self, user):
        access_token = await self.auth.create_access_token(
            subject=user.username, expires_time=timedelta(minutes=10)
        )
        refresh_token = await self.auth.create_refresh_token(
            subject=user.username, expires_time=timedelta(days=10)
        )

        return access_token, refresh_token

    async def set_in_cookies(self, access_token, refresh_token, response):
        await self.auth.set_access_cookies(access_token, response)
        await self.auth.set_refresh_cookies(refresh_token, response)

    async def refresh(self, user, response):
        await self.auth.jwt_refresh_token_required()

        access_token, refresh_token = await self.create(user)
        await self.set_in_cookies(access_token, refresh_token, response)
        return {"msg": "Successfully logged in"}


auth_dep = AuthJWTBearer()


def get_tokens(auth: AuthJWT = Depends(auth_dep)) -> Tokens:
    return Tokens(auth)
