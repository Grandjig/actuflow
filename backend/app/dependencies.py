"""FastAPI Dependencies.

Dependency injection for database sessions, authentication, etc.
"""

import uuid
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.config import settings
from app.models.user import User
from app.services.auth_service import decode_token


# =============================================================================
# Security
# =============================================================================

security = HTTPBearer(auto_error=False)


# =============================================================================
# Database Session
# =============================================================================

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


# =============================================================================
# Authentication
# =============================================================================

async def get_current_user(
    db: DBSession,
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> User:
    """Get the current authenticated user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )
    
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == user_uuid)
        .where(User.is_active == True)
        .where(User.is_deleted == False)
    )
    user = result.unique().scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user


async def get_optional_user(
    db: DBSession,
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> Optional[User]:
    """Get the current user if authenticated, otherwise None."""
    if not credentials:
        return None
    
    try:
        return await get_current_user(db, credentials)
    except HTTPException:
        return None


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[Optional[User], Depends(get_optional_user)]


# =============================================================================
# Permission Checking
# =============================================================================

def require_permission(resource: str, action: str):
    """Dependency that checks if user has a specific permission."""
    async def permission_checker(
        current_user: CurrentUser,
    ) -> User:
        # Superusers have all permissions
        if current_user.is_superuser:
            return current_user
        
        # Check role permissions
        if current_user.role:
            for perm in current_user.role.permissions:
                if perm.resource == resource and perm.action == action:
                    return current_user
                # Wildcard permission
                if perm.resource == "*" or perm.action == "*":
                    return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {resource}:{action}",
        )
    
    return permission_checker


def require_any_permission(*permissions: tuple[str, str]):
    """Dependency that checks if user has any of the specified permissions."""
    async def permission_checker(
        current_user: CurrentUser,
    ) -> User:
        if current_user.is_superuser:
            return current_user
        
        if current_user.role:
            for perm in current_user.role.permissions:
                for resource, action in permissions:
                    if perm.resource == resource and perm.action == action:
                        return current_user
                    if perm.resource == "*" or perm.action == "*":
                        return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    
    return permission_checker


# =============================================================================
# Pagination
# =============================================================================

class PaginationParams:
    """Pagination parameters."""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size


Pagination = Annotated[PaginationParams, Depends()]
