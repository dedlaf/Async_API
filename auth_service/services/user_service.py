from fastapi import Depends, HTTPException, status
from hash import verify_password
from schemas.user import UserCreateSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import User
from db.session import get_db
from services.login_history_service import LoginHistoryService


class UserService:
    def __init__(self, db: Session) -> None:
        self.__db = db
        self.__login_history_service = LoginHistoryService(db)

    def create_user(self, user: UserCreateSchema) -> User:
        if self.get_user(user.username):
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

    def get_user(self, username: str) -> User:
        return self.__db.query(User).filter(User.username == username).first()

    def login_user(self, username: str, password: str) -> User:
        user = self.get_user(username)
        password = verify_password(password, user.password)

        if user and password:
            self.__login_history_service.save_login_history(user.id)

            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
