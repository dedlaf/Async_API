import uuid
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Role, User
from db.session import get_db
from schemas.role import RoleCreateSchema, RoleUpdateSchema


class UserService:

    def __init__(self, db: Session) -> None:
        self.__db = db

    def get_user(self, login: str) -> Optional[Role]:
        return self.__db.query(User).filter(User.login == login).first()


def get_user(db: Session = Depends(get_db)):
    return UserService(db)
