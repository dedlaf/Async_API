from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


class UserInDB(User):
    id: str
