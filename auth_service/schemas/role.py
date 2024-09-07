import uuid

from pydantic import BaseModel


class RoleBaseSchema(BaseModel):
    name: str


class RoleCreateSchema(RoleBaseSchema): ...


class RoleUpdateSchema(RoleBaseSchema): ...


class RoleResponseSchema(RoleBaseSchema): ...


class RoleSchema(RoleBaseSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True
