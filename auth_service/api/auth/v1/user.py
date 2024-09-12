import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from db.models import User
from schemas.user import (
    RoleAssignationRequestSchema,
    RoleRevocationRequestSchema,
    UserLoginHistoryResponseSchema,
    UserResponseSchema,
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
)
async def get_history(
    user_id: uuid.UUID,
    login_history_service: LoginHistoryService = Depends(get_login_history_service),
):
    login_history = login_history_service.get_login_history(user_id)
    logged_date = [history.logged_date for history in login_history]

    response = UserLoginHistoryResponseSchema(date=logged_date)

    return response


@router.put(
    "/role/assign", response_model=UserResponseSchema, status_code=status.HTTP_200_OK
)
async def assign_role(
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
    "/role/revoke", response_model=UserResponseSchema, status_code=status.HTTP_200_OK
)
async def revoke_role(
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
