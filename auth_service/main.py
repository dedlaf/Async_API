import logging
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from http import HTTPStatus
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

class User(BaseModel):
    username: str = 'test'
    password: str = 'test'
class Tokens:
    def __init__(self, auth: AuthJWT):
        self.auth = auth

    async def validate(self):
        await self.auth.jwt_required()
        return await self.auth.get_jwt_subject()

    async def create(self, user):
        access_token = await self.auth.create_access_token(subject=user.username, expires_time=timedelta(minutes=1))
        refresh_token = await self.auth.create_refresh_token(subject=user.username, expires_time=timedelta(days=30))

        return access_token, refresh_token

    async def set_in_cookies(self, access_token, refresh_token, response):
        await self.auth.set_access_cookies(access_token, response)
        await self.auth.set_refresh_cookies(refresh_token, response)

    async def refresh(self, user, response):
        await self.auth.jwt_refresh_token_required()
        access_token, refresh_token = await self.create(user)
        await self.set_in_cookies(access_token, refresh_token, response)
        return {"msg": "Successfully logged in"}


app = FastAPI()
auth_dep = AuthJWTBearer()


def get_tokens(auth: AuthJWT = Depends(auth_dep)) -> Tokens:
    return Tokens(auth)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.post("/auth/login")
async def login(user: User, response: Response, tokens: Tokens = Depends(get_tokens)):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token, refresh_token = await tokens.create(user)
    await tokens.set_in_cookies(access_token, refresh_token, response)
    return {"msg": "Successfully logged in"}

us = User()
@app.get("/auth/refresh")
async def refresh(response: Response, user: User = us, tokens: Tokens = Depends(get_tokens)):
    return await tokens.refresh(user, response)



@app.get("/auth/user")
async def user(tokens: Tokens = Depends(get_tokens)):
    print('im here')
    current_user = await tokens.validate()
    return {"user": current_user} if current_user is not None else 404


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8070)
