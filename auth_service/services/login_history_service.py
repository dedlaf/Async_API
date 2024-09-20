import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from user_agents import parse

from db.models import LoginHistory
from db.session import get_db


class LoginHistoryService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def save_login_history(self, user_id: uuid.UUID, user_agent: str) -> None:
        try:
            login_history = LoginHistory(
                user_id=user_id,
                user_device_type=self.__get_user_device_type(user_agent),
                user_agent=user_agent,
            )

            self.__db.add(login_history)
            self.__db.commit()
            self.__db.refresh(login_history)

        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while creating the login history: {e}",
            )

    def get_login_history(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> list[LoginHistory]:
        return (
            self.__db.query(LoginHistory)
            .filter(LoginHistory.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def __get_user_device_type(self, user_agent: str) -> str:
        user_agent = parse(user_agent)
        device_type = "web"

        if user_agent.is_mobile:
            device_type = "mobile"

        if user_agent.is_pc:
            device_type = "web"

        return device_type


def get_login_history_service(db: Session = Depends(get_db)) -> LoginHistoryService:
    return LoginHistoryService(db)
