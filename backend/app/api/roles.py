"""Role API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.models.role import Role, Permission
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionResponse,
)
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("", response_model=list[RoleResponse])
async def list_roles(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "read"))],
):
    """List all roles."""
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .order_by(Role.name)
    )
    return list(result.unique().scalars().all())


@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "read"))],
):
    """List all permissions."""
    result = await db.execute(
        select(Permission).order_by(Permission.resource, Permission.action)
    )
    return list(result.scalars().all())


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "read"))],
):
    """Get a role by ID."""
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .where(Role.id == role_id)
    )
    role = result.unique().scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    return role


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "create"))],
):
    """Create a new role."""
    audit_service = AuditService(db)
    
    # Check for duplicate name
    result = await db.execute(
        select(Role).where(Role.name == role_data.name)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name already exists",
        )
    
    # Get permissions
    permissions = []
    if role_data.permission_ids:
        perm_result = await db.execute(
            select(Permission).where(Permission.id.in_(role_data.permission_ids))
        )
        permissions = list(perm_result.scalars().all())
    
    role = Role(
        name=role_data.name,
        description=role_data.description,
        is_system=False,
    )
    role.permissions = permissions
    
    db.add(role)
    await db.flush()
    await db.refresh(role)
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="role",
        resource_id=role.id,
        new_values={"name": role.name},
    )
    
    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: uuid.UUID,
    role_data: RoleUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "update"))],
):
    """Update a role."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
        .where(Role.id == role_id)
    )
    role = result.unique().scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify system role",
        )
    
    if role_data.name:
        role.name = role_data.name
    if role_data.description is not None:
        role.description = role_data.description
    
    if role_data.permission_ids is not None:
        perm_result = await db.execute(
            select(Permission).where(Permission.id.in_(role_data.permission_ids))
        )
        role.permissions = list(perm_result.scalars().all())
    
    await db.flush()
    await db.refresh(role)
    
    await audit_service.log(
        user_id=current_user.id,
        action="update",
        resource_type="role",
        resource_id=role_id,
        new_values=role_data.model_dump(exclude_unset=True),
    )
    
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("role", "delete"))],
):
    """Delete a role."""
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system role",
        )
    
    # Check if any users have this role
    user_count_result = await db.execute(
        select(User).where(User.role_id == role_id, User.is_deleted == False)
    )
    if user_count_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete role with assigned users",
        )
    
    await db.delete(role)
    await db.flush()
    
    await audit_service.log(
        user_id=current_user.id,
        action="delete",
        resource_type="role",
        resource_id=role_id,
    )
