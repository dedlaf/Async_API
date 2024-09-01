from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from schemas.role import RoleCreate, RoleUpdate, RoleOut
# from models.role import Role
#
# router = APIRouter()
#
#
# @router.post("/", response_model=RoleOut)
# def create_role(role: RoleCreate, db: Session = Depends(get_db)):
#     db_role = Role(name=role.name)
#     db.add(db_role)
#     db.commit()
#     db.refresh(db_role)
#
#     return db_role
#
#
# @router.get("/{role_id}", response_model=RoleOut)
# def get_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
#     role = db.query(Role).filter(Role.id == role_id).first()
#
#     if not role:
#         raise HTTPException(status_code=404, detail="Role not found")
#
#     return role
#
#
# @router.get("/", response_model=list[RoleOut])
# def get_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     roles = db.query(Role).offset(skip).limit(limit).all()
#
#     return roles
#
#
# @router.put("/{role_id}", response_model=RoleOut)
# def update_role(role_id: uuid.UUID, role: RoleUpdate, db: Session = Depends(get_db)):
#     db_role = db.query(Role).filter(Role.id == role_id).first()
#
#     if not db_role:
#         raise HTTPException(status_code=404, detail="Role not found")
#
#     for key, value in role.dict(exclude_unset=True).items():
#         setattr(db_role, key, value)
#
#     db.commit()
#     db.refresh(db_role)
#
#     return db_role
#
#
# @router.delete("/{role_id}", response_model=RoleOut)
# def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
#     role = db.query(Role).filter(Role.id == role_id).first()
#
#     if not role:
#         raise HTTPException(status_code=404, detail="Role not found")
#
#     db.delete(role)
#     db.commit()
#     return role