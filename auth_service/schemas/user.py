from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    email: str
    password: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserLogoutSchema(UserBaseSchema): ...


class UserResponseSchema(UserBaseSchema): ...
