import uuid

from fastapi import Depends, HTTPException, status
from hash import verify_password
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Role, User
from db.session import get_db
from schemas.user import UserCreateSchema
from services.login_history_service import LoginHistoryService


class UserService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def create_user(self, user: UserCreateSchema) -> User:
        if self.get_user_by_username(user.username):
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

    def get_user_by_username(self, username: str) -> User:
        return self.__db.query(User).filter(User.username == username).first()

    def get_user(self, user_id: uuid.UUID) -> User:
        return self.__db.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id: uuid.UUID) -> User:
        try:
            user = self.get_user(user_id)

            if user:
                self.__db.delete(user)
                self.__db.commit()

            return user
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while deleting user: {e}",
            )

    def login_user(self, username: str, password: str, user_agent: str) -> User:
        user = self.get_user_by_username(username)
        password = verify_password(password, user.password)

        if user and password:
            login_history_service = LoginHistoryService(self.__db)
            login_history_service.save_login_history(user.id, user_agent)

            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )

    def assign_role(self, user: User, role: Role) -> User:
        try:
            user.role_id = role.id
            self.__db.commit()
            self.__db.refresh(user)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while assign role to user: {e}",
            )

        return user

    def revoke_role(self, user: User) -> User:
        try:
            user.role_id = None
            self.__db.commit()
            self.__db.refresh(user)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while revoking user role: {e}",
            )

        return user

    def has_role(self, user: User, role: Role) -> bool:
        return (
            self.__db.query(User)
            .join(User.role)
            .filter(User.id == user.id, Role.name == role.name)
            .first()
            is not None
        )


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
