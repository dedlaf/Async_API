from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from http import HTTPStatus
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

app = FastAPI()
auth_dep = AuthJWTBearer()


class User(BaseModel):
    username: str
    password: str


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
async def login(user: User, response: Response, authorize: AuthJWT = Depends(auth_dep)):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = await authorize.create_access_token(subject=user.username, expires_time=timedelta(minutes=15))
    refresh_token = await authorize.create_refresh_token(subject=user.username, expires_time=timedelta(days=30))
    await authorize.set_access_cookies(access_token, response)
    await authorize.set_refresh_cookies(refresh_token, response)
    return {"msg": "Successfully logged in"}


@app.get("/auth/user")
async def user(authorize: AuthJWT = Depends(auth_dep)):
    await authorize.jwt_required()

    current_user = await authorize.get_jwt_subject()
    return {"user": current_user}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("basic:app", host="0.0.0.0", port=8070)
