from pydantic import UUID4, BaseModel


class Role(BaseModel):
    id: UUID4
    name: str


class RoleUpdate(BaseModel):
    name: str


class RoleResponse(Role):
    ...
