import uuid

from fastapi import APIRouter, Depends, HTTPException

from db.session import get_db
from schemas.role import RoleUpdate, RoleResponse
from sqlalchemy.orm import Session

from schemas.role import Role
from services.role_service import RoleService, get_role_service

router = APIRouter()


@router.post("/", response_model=RoleResponse)
async def create_role(role_name: str, role_service: RoleService = Depends(get_role_service)):
    role = role_service.create_role(role_name)
    return role


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


@router.get("/", response_model=list[RoleResponse])
async def get_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()

    return roles


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: uuid.UUID, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()

    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in role.dict(exclude_unset=True).items():
        setattr(db_role, key, value)

    db.commit()
    db.refresh(db_role)

    return db_role


@router.delete("/{role_id}", response_model=RoleResponse)
def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
    return role
