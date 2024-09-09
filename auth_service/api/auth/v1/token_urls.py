from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException, Response

from core.config.components.settings import Settings, User
from core.config.components.token_conf import Tokens, get_tokens

router = APIRouter()


@AuthJWT.load_config
def get_config():
    return Settings()


@router.get("/refresh")
async def refresh(
    response: Response, user: User = User(), tokens: Tokens = Depends(get_tokens)
):
    return await tokens.refresh(user, response)


@router.get("/user")
async def user(tokens: Tokens = Depends(get_tokens)):
    current_user = await tokens.validate()
    return {"user": current_user} if current_user is not None else 404
