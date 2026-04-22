"""FastAPI Dependencies.

Dependency injection functions for routes.
"""

import uuid
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.user import User
from app.services.auth_service import AuthService
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Type aliases
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    """Get the current authenticated user."""
    auth_service = AuthService(db)
    
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await auth_service.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_permission(resource: str, action: str) -> Callable:
    """Create a dependency that requires a specific permission."""
    
    async def check_permission(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.is_superuser:
            return current_user
        
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned",
            )
        
        # Check permissions
        for perm in current_user.role.permissions:
            if perm.resource == resource and perm.action == action:
                return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {resource}:{action}",
        )
    
    return check_permission


def require_role(*allowed_roles: str) -> Callable:
    """Create a dependency that requires one of the specified roles."""
    
    async def check_role(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.is_superuser:
            return current_user
        
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned",
            )
        
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {current_user.role.name} not allowed",
            )
        
        return current_user
    
    return check_role


async def get_optional_user(
    token: Annotated[str | None, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False))],
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> User | None:
    """Get the current user if authenticated, None otherwise."""
    if not token:
        return None
    
    try:
        auth_service = AuthService(db)
        payload = auth_service.decode_token(token)
        if payload and payload.get("type") == "access":
            user_id = payload.get("sub")
            if user_id:
                return await auth_service.get_user_by_id(uuid.UUID(user_id))
    except Exception:
        pass
    
    return None
