"""
Users API Routes
================

User management endpoints.
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
from app.api.auth import get_password_hash
from app.models.user import User
from app.models.role import Role
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListItem,
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserListItem])
async def list_users(
    db: DBSession,
    pagination: Pagination,
    current_user: CurrentUser,
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    role_id: Optional[UUID] = Query(None),
):
    """List users with pagination and filtering."""
    # Build query
    query = select(User).where(User.is_deleted == False)

    if search:
        query = query.where(
            User.email.ilike(f"%{search}%") | User.full_name.ilike(f"%{search}%")
        )

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if role_id:
        query = query.where(User.role_id == role_id)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = (
        query
        .options(selectinload(User.role))
        .offset(pagination.offset)
        .limit(pagination.page_size)
        .order_by(User.created_at.desc())
    )
    result = await db.execute(query)
    users = result.scalars().all()

    items = [
        UserListItem(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            department=user.department,
            role_name=user.role.name if user.role else None,
            is_active=user.is_active,
            last_login=user.last_login,
        )
        for user in users
    ]

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    db: DBSession,
    user_id: UUID,
    current_user: CurrentUser,
):
    """Get a specific user by ID."""
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.is_deleted == False)
        .options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    db: DBSession,
    user_data: UserCreate,
    _: CurrentUser = Depends(require_permission("user", "create")),
):
    """Create a new user."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Validate role exists
    if user_data.role_id:
        result = await db.execute(select(Role).where(Role.id == user_data.role_id))
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role_id",
            )

    # Create user
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        department=user_data.department,
        job_title=user_data.job_title,
        role_id=user_data.role_id,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user, ["role"])

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    db: DBSession,
    user_id: UUID,
    user_data: UserUpdate,
    _: CurrentUser = Depends(require_permission("user", "update")),
):
    """Update an existing user."""
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    if "email" in update_data and update_data["email"] != user.email:
        # Check if new email is taken
        result = await db.execute(
            select(User).where(User.email == update_data["email"])
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user, ["role"])

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: DBSession,
    user_id: UUID,
    current_user: CurrentUser = Depends(require_permission("user", "delete")),
):
    """Soft delete a user."""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_deleted = True
    user.is_active = False
