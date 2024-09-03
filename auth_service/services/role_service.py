from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.role import Role


class RoleService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def create_role(self, role_name: str) -> Role: ...

    def get_role(self, role_id: str) -> Role: ...

    def get_roles(self) -> list[Role]: ...

    def update_role(self, role_id: str, role: str) -> Role: ...

    def delete_role(self, role_id: str) -> Role: ...


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)

