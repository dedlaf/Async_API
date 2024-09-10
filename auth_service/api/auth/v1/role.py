import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.role import RoleCreateSchema, RoleResponseSchema, RoleUpdateSchema
from services.role_service import RoleService, get_role_service

router = APIRouter()


@router.post(
    "/", response_model=RoleResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_role(
    role: RoleCreateSchema, role_service: RoleService = Depends(get_role_service)
):
    new_role = role_service.create_role(role)

    return new_role


@router.get(
    "/{role_id}", response_model=RoleResponseSchema, status_code=status.HTTP_200_OK
)
async def get_role(
    role_id: uuid.UUID, role_service: RoleService = Depends(get_role_service)
):
    role = role_service.get_role(role_id)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return role


@router.get(
    "/", response_model=list[RoleResponseSchema], status_code=status.HTTP_200_OK
)
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    role_service: RoleService = Depends(get_role_service),
):
    roles = role_service.get_roles(skip=skip, limit=limit)

    return roles


@router.put(
    "/{role_id}", response_model=RoleResponseSchema, status_code=status.HTTP_200_OK
)
async def update_role(
    role_id: uuid.UUID,
    role_update: RoleUpdateSchema,
    role_service: RoleService = Depends(get_role_service),
):
    updated_role = role_service.update_role(role_id, role_update)

    if not updated_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return updated_role


@router.delete(
    "/{role_id}", response_model=RoleResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_role(
    role_id: uuid.UUID, role_service: RoleService = Depends(get_role_service)
):
    deleted_role = role_service.delete_role(role_id)

    if not deleted_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return deleted_role
