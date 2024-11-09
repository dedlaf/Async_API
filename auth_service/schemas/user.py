import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    email: str
    password: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserLogoutSchema(UserBaseSchema): ...


class UserResponseSchema(UserBaseSchema):
    id: Optional[uuid.UUID] = None
    role_id: Optional[uuid.UUID] = None

class UserResponseAdminSchema(UserBaseSchema):
    role_id: Optional[uuid.UUID] = None
    email: str


class RoleAssignationRequestSchema(BaseModel):
    user_id: uuid.UUID
    role_name: str


class UsersRoleRequestSchema(BaseModel):
    role_name: str


class RoleRevocationRequestSchema(BaseModel):
    user_id: uuid.UUID


class UserLoginHistoryResponseSchema(BaseModel):
    date: list[datetime]


class GetUserInfoResponseSchema(BaseModel):
    id: uuid.UUID
    username: str
    role_id: uuid.UUID
    email: str