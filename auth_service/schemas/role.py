from pydantic import BaseModel, UUID4


class Role(BaseModel):
    id: UUID4
    name: str


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: str


class RoleOut(BaseModel):
    id: UUID4
    name: str

    class Config:
        orm_mode = True
