import uuid
from datetime import datetime

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
    id: uuid.UUID
    role_id: uuid.UUID


class UserResponseAdminSchema(UserBaseSchema):
    role_id: uuid.UUID
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
