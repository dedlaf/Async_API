from fastapi import Depends, HTTPException, Response, APIRouter
from async_fastapi_jwt_auth import AuthJWT
from core.config.components.token_conf import Tokens, get_tokens
from core.config.components.settings import Settings, User


router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/login")
async def login(user: User, response: Response, tokens: Tokens = Depends(get_tokens)):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token, refresh_token = await tokens.create(user)
    await tokens.set_in_cookies(access_token, refresh_token, response)
    return {"msg": "Successfully logged in"}


@router.get("/refresh")
async def refresh(response: Response, user: User = User(), tokens: Tokens = Depends(get_tokens)):
    return await tokens.refresh(user, response)


@router.get("/user")
async def user(tokens: Tokens = Depends(get_tokens)):
    current_user = await tokens.validate()
    return {"user": current_user} if current_user is not None else 404
