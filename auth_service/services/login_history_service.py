import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import LoginHistory
from db.session import get_db


class LoginHistoryService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def save_login_history(self, user_id: uuid.UUID) -> None:
        try:
            login_history = LoginHistory(user_id)

            self.__db.add(login_history)
            self.__db.commit()
            self.__db.refresh(login_history)

        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while creating the login history: {e}",
            )


def get_login_history_service(db: Session = Depends(get_db)) -> LoginHistoryService:
    return LoginHistoryService(db)
