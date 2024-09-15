import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Request
from redis.asyncio import Redis

from core.config.components.role_decorator import has_admin
from core.config.components.token_conf import Tokens, get_tokens
from db.redis import get_redis
from hash import hash_data
from schemas.user import (
    RoleAssignationRequestSchema,
    RoleRevocationRequestSchema,
    UserLoginHistoryResponseSchema,
    UserResponseSchema,
    UsersRoleRequestSchema,
)
from services.login_history_service import (
    LoginHistoryService,
    get_login_history_service,
)
from services.role_service import RoleService, get_role_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.get(
    "/history/{user_id}",
    response_model=UserLoginHistoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get login history of user",
)
async def get_history(
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    login_history_service: LoginHistoryService = Depends(get_login_history_service),
):
    login_history = login_history_service.get_login_history(
        user_id, skip=skip, limit=limit
    )
    logged_date = [history.logged_date for history in login_history]

    response = UserLoginHistoryResponseSchema(date=logged_date)

    return response


@router.put(
    "/role/assign",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Assign role to user",
)
@has_admin
async def assign_role(
    request: Request,
    role_assignation: RoleAssignationRequestSchema,
    role_service: RoleService = Depends(get_role_service),
    user_service: UserService = Depends(get_user_service),
):
    role = role_service.get_role_by_name(role_assignation.role_name)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    user = user_service.get_user(role_assignation.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = user_service.assign_role(user, role)

    return user


@router.put(
    "/role/revoke",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Revoke role of user",
)
@has_admin
async def revoke_role(
    request: Request,
    role_assignation: RoleRevocationRequestSchema,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user(role_assignation.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = user_service.revoke_role(user)

    return user


@router.post(
    "/role/has_role",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Check role of user",
)
async def has_role(
        request: Request,
        role_assignation: UsersRoleRequestSchema,
        redis: Redis = Depends(get_redis),
        tokens: Tokens = Depends(get_tokens),
        role_service: RoleService = Depends(get_role_service),
        user_service: UserService = Depends(get_user_service),
):
    access_token = request.cookies.get('access_token_cookie')

    curr_user = await tokens.get_sub(access_token)

    if not curr_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

    user_agent = request.headers.get("user-agent")
    byte_agent = bytes(user_agent, encoding="utf-8")
    storage_token = await redis.get(f"access_token:{curr_user}:{hash_data(byte_agent)}")

    if not storage_token or (storage_token.decode() != str(access_token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

    user = user_service.get_user_by_username(curr_user)
    role = role_service.get_role_by_name(role_assignation.role_name)

    if user and role and user_service.has_role(user, role):
        return user
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not needed role"
        )


@router.delete(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Delete user",
)
@has_admin
async def delete_user(
    request: Request,
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.delete_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
