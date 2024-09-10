from fastapi import status, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import User
from hash import verify_password
from schemas.user import UserCreateSchema
from db.session import get_db


class UserService:
    def __init__(self, db: Session):
        self.__db = db

    def create_user(self, user: UserCreateSchema) -> User:
        if self.get_user(user.login):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        try:
            user = User(**user.dict())

            self.__db.add(user)
            self.__db.commit()
            self.__db.refresh(user)

            return user
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while creating the user: {e}",
            )

    def get_user(self, login: str) -> User:
        return self.__db.query(User).filter(User.login == login).first()

    def login_user(self, login: str, password: str) -> User:
        user = self.get_user(login)
        password = verify_password(password, user.password)

        if user and password:
            return user

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login or password")


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
