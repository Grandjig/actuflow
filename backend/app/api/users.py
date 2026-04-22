"""User API Routes."""

import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.dependencies import get_current_user, require_permission
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("", response_model=UserListResponse)
async def list_users(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("user", "read"))],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    role_id: Optional[uuid.UUID] = None,
):
    """List users."""
    query = select(User).options(selectinload(User.role)).where(User.is_deleted == False)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (User.email.ilike(search_term)) | (User.full_name.ilike(search_term))
        )
    
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    
    if role_id:
        query = query.where(User.role_id == role_id)
    
    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    users = list(result.unique().scalars().all())
    
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("user", "read"))],
):
    """Get a user by ID."""
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == user_id, User.is_deleted == False)
    )
    user = result.unique().scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("user", "create"))],
):
    """Create a new user."""
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    
    # Check for existing email
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=auth_service.hash_password(user_data.password),
        role_id=user_data.role_id,
        department=user_data.department,
        job_title=user_data.job_title,
        is_active=user_data.is_active if user_data.is_active is not None else True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    
    await audit_service.log(
        user_id=current_user.id,
        action="create",
        resource_type="user",
        resource_id=user.id,
        new_values={"email": user.email, "full_name": user.full_name},
    )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("user", "update"))],
):
    """Update a user."""
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Handle password separately
    if "password" in update_data:
        user.hashed_password = auth_service.hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    await db.flush()
    await db.refresh(user)
    
    await audit_service.log(
        user_id=current_user.id,
        action="update",
        resource_type="user",
        resource_id=user_id,
        new_values=user_data.model_dump(exclude_unset=True, exclude={"password"}),
    )
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[User, Depends(require_permission("user", "delete"))],
):
    """Delete a user (soft delete)."""
    audit_service = AuditService(db)
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )
    
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user.is_deleted = True
    user.is_active = False
    await db.flush()
    
    await audit_service.log(
        user_id=current_user.id,
        action="delete",
        resource_type="user",
        resource_id=user_id,
    )
