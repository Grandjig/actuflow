"""
Roles API Routes
================

Role and permission management endpoints.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.dependencies import (
    DBSession,
    CurrentUser,
    Pagination,
    require_permission,
)
from app.models.role import Role, Permission, role_permissions
from app.schemas.user import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionResponse,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=list[RoleResponse])
async def list_roles(
    db: DBSession,
    current_user: CurrentUser,
):
    """List all roles."""
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).order_by(Role.name)
    )
    roles = result.scalars().all()
    return roles


@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    db: DBSession,
    current_user: CurrentUser,
):
    """List all available permissions."""
    result = await db.execute(
        select(Permission).order_by(Permission.resource, Permission.action)
    )
    permissions = result.scalars().all()
    return permissions


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    db: DBSession,
    role_id: UUID,
    current_user: CurrentUser,
):
    """Get a specific role by ID."""
    result = await db.execute(
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.permissions))
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    return role


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    db: DBSession,
    role_data: RoleCreate,
    _: CurrentUser = Depends(require_permission("role", "create")),
):
    """Create a new role."""
    # Check if name already exists
    result = await db.execute(select(Role).where(Role.name == role_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role with this name already exists",
        )

    # Create role
    role = Role(
        name=role_data.name,
        description=role_data.description,
        is_system=False,
    )

    # Add permissions
    if role_data.permission_ids:
        result = await db.execute(
            select(Permission).where(Permission.id.in_(role_data.permission_ids))
        )
        permissions = result.scalars().all()
        role.permissions = list(permissions)

    db.add(role)
    await db.flush()
    await db.refresh(role, ["permissions"])

    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    db: DBSession,
    role_id: UUID,
    role_data: RoleUpdate,
    _: CurrentUser = Depends(require_permission("role", "update")),
):
    """Update an existing role."""
    result = await db.execute(
        select(Role)
        .where(Role.id == role_id)
        .options(selectinload(Role.permissions))
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role.is_system and role_data.name and role_data.name != role.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot rename system roles",
        )

    # Update fields
    if role_data.name is not None:
        role.name = role_data.name
    if role_data.description is not None:
        role.description = role_data.description

    # Update permissions
    if role_data.permission_ids is not None:
        result = await db.execute(
            select(Permission).where(Permission.id.in_(role_data.permission_ids))
        )
        permissions = result.scalars().all()
        role.permissions = list(permissions)

    await db.flush()
    await db.refresh(role, ["permissions"])

    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    db: DBSession,
    role_id: UUID,
    _: CurrentUser = Depends(require_permission("role", "delete")),
):
    """Delete a role."""
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system roles",
        )

    await db.delete(role)
