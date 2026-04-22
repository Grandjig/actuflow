"""
User Management API Routes
==========================

CRUD operations for users.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import (
    CurrentUser,
    DBSession,
    Pagination,
    Sorting,
    require_permission,
    require_role,
)
from app.schemas.common import PaginatedResponse, SuccessMessage
from app.schemas.user import (
    UserCreate,
    UserListItem,
    UserPreferencesUpdate,
    UserProfile,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserListItem])
async def list_users(
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    sorting: Sorting,
    search: Optional[str] = Query(default=None, max_length=100),
    role_id: Optional[UUID] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    _: None = Depends(require_permission("user", "read")),
):
    """
    List all users with pagination and filtering.
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    
    users, total = await service.list_users(
        search=search,
        role_id=role_id,
        department=department,
        is_active=is_active,
        offset=pagination.offset,
        limit=pagination.limit,
        sort_by=sorting.sort_by,
        sort_order=sorting.sort_order,
    )
    
    return PaginatedResponse.create(
        items=users,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("user", "read")),
):
    """
    Get a specific user by ID.
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    target_user = await service.get_user(user_id)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return target_user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("user", "create")),
):
    """
    Create a new user.
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    
    # Check if email already exists
    existing = await service.get_user_by_email(user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    
    new_user = await service.create_user(user_data, created_by=user)
    
    return new_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("user", "update")),
):
    """
    Update a user.
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    
    target_user = await service.get_user(user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check email uniqueness if changing
    if user_data.email and user_data.email != target_user.email:
        existing = await service.get_user_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
    
    updated_user = await service.update_user(
        target_user,
        user_data,
        updated_by=user,
    )
    
    return updated_user


@router.delete("/{user_id}", response_model=SuccessMessage)
async def delete_user(
    user_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_permission("user", "delete")),
):
    """
    Soft delete a user.
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    
    target_user = await service.get_user(user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if target_user.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )
    
    await service.delete_user(target_user)
    
    return SuccessMessage(message="User deleted successfully")


@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: UUID,
    role_id: UUID,
    db: DBSession,
    user: CurrentUser,
    _: None = Depends(require_role("admin")),
):
    """
    Update a user's role (admin only).
    """
    from app.services.user_service import UserService
    
    service = UserService(db)
    
    target_user = await service.get_user(user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    updated_user = await service.update_user_role(
        target_user,
        role_id,
        updated_by=user,
    )
    
    return updated_user


@router.put("/{user_id}/preferences", response_model=UserProfile)
async def update_user_preferences(
    user_id: UUID,
    preferences: UserPreferencesUpdate,
    db: DBSession,
    user: CurrentUser,
):
    """
    Update user preferences.
    
    Users can only update their own preferences unless admin.
    """
    from app.services.user_service import UserService
    
    # Check permission
    if user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update another user's preferences",
        )
    
    service = UserService(db)
    
    target_user = await service.get_user(user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    updated_user = await service.update_preferences(target_user, preferences)
    
    return updated_user


@router.get("/{user_id}/activity")
async def get_user_activity(
    user_id: UUID,
    db: DBSession,
    user: CurrentUser,
    pagination: Pagination,
    _: None = Depends(require_permission("user", "read")),
):
    """
    Get a user's recent activity from audit log.
    """
    from app.services.audit_service import AuditService
    
    service = AuditService(db)
    
    activities, total = await service.get_user_activity(
        user_id=user_id,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=activities,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )
