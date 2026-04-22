"""
Role Management API Routes
==========================

CRUD operations for roles and permissions.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import CurrentUser, DBSession, require_role
from app.schemas.common import PaginatedResponse, SuccessMessage
from app.schemas.user import (
    PermissionResponse,
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)

router = APIRouter()


@router.get("", response_model=list[RoleResponse])
async def list_roles(
    db: DBSession,
    user: CurrentUser,
):
    """
    List all roles.
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    roles = await service.list_roles()
    
    return roles


@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    db: DBSession,
    user: CurrentUser,
):
    """
    List all available permissions.
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    permissions = await service.list_permissions()
    
    return permissions


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: UUID,
    db: DBSession,
    user: CurrentUser,
):
    """
    Get a specific role by ID.
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    role = await service.get_role(role_id)
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    return role


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_role("admin")),
):
    """
    Create a new role (admin only).
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    
    # Check if name already exists
    existing = await service.get_role_by_name(role_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role with this name already exists",
        )
    
    role = await service.create_role(role_data)
    
    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_role("admin")),
):
    """
    Update a role (admin only).
    
    System roles cannot be modified.
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System roles cannot be modified",
        )
    
    # Check name uniqueness if changing
    if role_data.name and role_data.name != role.name:
        existing = await service.get_role_by_name(role_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role with this name already exists",
            )
    
    updated_role = await service.update_role(role, role_data)
    
    return updated_role


@router.delete("/{role_id}", response_model=SuccessMessage)
async def delete_role(
    role_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_role("admin")),
):
    """
    Delete a role (admin only).
    
    System roles cannot be deleted.
    Roles with assigned users cannot be deleted.
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System roles cannot be deleted",
        )
    
    # Check if any users have this role
    user_count = await service.get_role_user_count(role_id)
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role with {user_count} assigned users",
        )
    
    await service.delete_role(role)
    
    return SuccessMessage(message="Role deleted successfully")


@router.put("/{role_id}/permissions", response_model=RoleResponse)
async def update_role_permissions(
    role_id: UUID,
    permission_ids: list[UUID],
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_role("admin")),
):
    """
    Update permissions for a role (admin only).
    """
    from app.services.role_service import RoleService
    
    service = RoleService(db)
    
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System role permissions cannot be modified",
        )
    
    updated_role = await service.update_permissions(role, permission_ids)
    
    return updated_role
