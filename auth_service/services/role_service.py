import uuid
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.models import Role
from db.session import get_db
from schemas.role import RoleCreateSchema, RoleUpdateSchema


class RoleService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def create_role(self, role: RoleCreateSchema) -> Role:
        try:
            role = Role(**role.dict())

            self.__db.add(role)
            self.__db.commit()
            self.__db.refresh(role)

            return role
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while creating the role: {e}",
            )

    def get_role(self, role_id: uuid.UUID) -> Optional[Role]:
        return self.__db.query(Role).filter(Role.id == role_id).first()

    def get_roles(self, skip: int = 0, limit: int = 100) -> list[Role]:
        return self.__db.query(Role).offset(skip).limit(limit).all()

    def update_role(
        self, role_id: uuid.UUID, role_update: RoleUpdateSchema
    ) -> Optional[Role]:
        try:
            role = self.get_role(role_id)

            if role:
                for key, value in role_update.dict(exclude_unset=True).items():
                    setattr(role, key, value)

                self.__db.commit()
                self.__db.refresh(role)

            return role
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while updating the role: {e}",
            )

    def delete_role(self, role_id: uuid.UUID) -> Optional[Role]:
        try:
            role = self.get_role(role_id)

            if role:
                self.__db.delete(role)
                self.__db.commit()

            return role
        except SQLAlchemyError as e:
            self.__db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while deleting the role: {e}",
            )


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)
