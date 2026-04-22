"""
FastAPI Dependencies
====================

Dependency injection functions for FastAPI endpoints.
"""

from typing import Annotated, AsyncGenerator, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import async_session_factory
from app.models.user import User
from app.schemas.common import PaginationParams

# =============================================================================
# Security
# =============================================================================

security = HTTPBearer(auto_error=False)


# =============================================================================
# Database Session
# =============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


DBSession = Annotated[AsyncSession, Depends(get_db)]


# =============================================================================
# Authentication
# =============================================================================

async def get_current_user_optional(
    db: DBSession,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User | None:
    """Get current user if authenticated, None otherwise."""
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    result = await db.execute(
        select(User)
        .where(User.id == UUID(user_id))
        .where(User.is_active == True)
        .options(selectinload(User.role))
    )
    return result.scalar_one_or_none()


async def get_current_user(
    user: User | None = Depends(get_current_user_optional),
) -> User:
    """Get current authenticated user (required)."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[User | None, Depends(get_current_user_optional)]


# =============================================================================
# Permission Checking
# =============================================================================

class PermissionChecker:
    """Dependency for checking user permissions."""

    def __init__(self, resource: str, action: str):
        self.resource = resource
        self.action = action

    async def __call__(self, current_user: CurrentUser) -> User:
        if current_user.is_superuser:
            return current_user

        if not current_user.has_permission(self.resource, self.action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {self.resource}:{self.action}",
            )
        return current_user


def require_permission(resource: str, action: str):
    """Dependency factory for requiring a specific permission."""
    return Depends(PermissionChecker(resource, action))


class RoleChecker:
    """Dependency for checking user roles."""

    def __init__(self, *allowed_roles: str):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: CurrentUser) -> User:
        if current_user.is_superuser:
            return current_user

        if current_user.role and current_user.role.name in self.allowed_roles:
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role required: {', '.join(self.allowed_roles)}",
        )


def require_role(*roles: str):
    """Dependency factory for requiring specific roles."""
    return Depends(RoleChecker(*roles))


# =============================================================================
# Pagination
# =============================================================================

async def get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=1, le=1000, description="Items per page"),
) -> PaginationParams:
    """Get pagination parameters."""
    return PaginationParams(page=page, page_size=page_size)


Pagination = Annotated[PaginationParams, Depends(get_pagination)]
