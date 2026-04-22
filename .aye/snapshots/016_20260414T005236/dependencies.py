"""
FastAPI Dependencies
====================

Dependency injection functions for FastAPI endpoints.
Provides database sessions, authentication, authorization, and service instances.
"""

from typing import Annotated, AsyncGenerator, Optional

import structlog
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings

logger = structlog.get_logger()

# =============================================================================
# Security Schemes
# =============================================================================

# HTTP Bearer token scheme
bearer_scheme = HTTPBearer(auto_error=False)


# =============================================================================
# Database Dependencies
# =============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session.
    
    Yields a SQLAlchemy async session that is automatically
    closed after the request completes.
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    # Import here to avoid circular imports
    from app.database import async_session_factory
    
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Type alias for database dependency
DBSession = Annotated[AsyncSession, Depends(get_db)]


# =============================================================================
# Authentication Dependencies
# =============================================================================

async def get_token_payload(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> dict:
    """
    Extract and validate JWT token payload.
    
    Supports both local JWT and Keycloak tokens based on configuration.
    
    Returns:
        Decoded token payload as dictionary.
        
    Raises:
        HTTPException: If token is missing, invalid, or expired.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    try:
        if settings.use_keycloak:
            # Validate against Keycloak
            # TODO: Implement Keycloak token validation
            # This would use python-keycloak to verify the token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,  # Would use Keycloak public key
                algorithms=[settings.JWT_ALGORITHM],
            )
        else:
            # Local JWT validation
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        
        return payload
        
    except JWTError as e:
        logger.warning("Invalid token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    payload: Annotated[dict, Depends(get_token_payload)],
    db: DBSession,
) -> "User":
    """
    Get the current authenticated user.
    
    Loads the full user object from database based on token payload.
    
    Returns:
        User model instance.
        
    Raises:
        HTTPException: If user not found or inactive.
    """
    # Import here to avoid circular imports
    from app.models.user import User
    from sqlalchemy import select
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    # Query user from database
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user


async def get_current_user_optional(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
    db: DBSession,
) -> Optional["User"]:
    """
    Get the current user if authenticated, None otherwise.
    
    Use this for endpoints that work both with and without authentication.
    """
    if credentials is None:
        return None
    
    try:
        payload = await get_token_payload(credentials)
        return await get_current_user(payload, db)
    except HTTPException:
        return None


# Type alias for current user dependency
CurrentUser = Annotated["User", Depends(get_current_user)]
OptionalUser = Annotated[Optional["User"], Depends(get_current_user_optional)]


# =============================================================================
# Authorization Dependencies
# =============================================================================

def require_role(*allowed_roles: str):
    """
    Dependency factory that requires user to have one of the specified roles.
    
    Usage:
        @app.get("/admin")
        async def admin_endpoint(
            user: CurrentUser,
            _: None = Depends(require_role("admin", "superuser"))
        ):
            ...
    """
    async def role_checker(user: CurrentUser) -> None:
        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role",
            )
        
        if user.role.name not in allowed_roles:
            logger.warning(
                "Access denied - insufficient role",
                user_id=str(user.id),
                user_role=user.role.name,
                required_roles=allowed_roles,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}",
            )
    
    return role_checker


def require_permission(resource: str, action: str):
    """
    Dependency factory that requires user to have a specific permission.
    
    Usage:
        @app.delete("/policies/{id}")
        async def delete_policy(
            user: CurrentUser,
            _: None = Depends(require_permission("policy", "delete"))
        ):
            ...
    """
    async def permission_checker(user: CurrentUser) -> None:
        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role",
            )
        
        # Check if user's role has the required permission
        has_permission = any(
            p.resource == resource and p.action == action
            for p in user.role.permissions
        )
        
        if not has_permission:
            logger.warning(
                "Access denied - missing permission",
                user_id=str(user.id),
                required_resource=resource,
                required_action=action,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {action} on {resource}",
            )
    
    return permission_checker


# =============================================================================
# Service Dependencies
# =============================================================================

async def get_redis():
    """
    Get Redis client.
    
    Returns:
        Redis client instance.
    """
    # Import here to avoid circular imports
    from app.core.redis import get_redis_client
    return await get_redis_client()


async def get_ai_service():
    """
    Get AI service client.
    
    Returns:
        AIService instance if AI is enabled, None otherwise.
        
    Raises:
        HTTPException: If AI is disabled but endpoint requires it.
    """
    if not settings.AI_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are disabled",
        )
    
    # Import here to avoid circular imports
    from app.services.ai_service import AIService
    return AIService()


async def get_ai_service_optional():
    """
    Get AI service client if available, None otherwise.
    
    Use this for endpoints that can work with or without AI.
    """
    if not settings.AI_ENABLED:
        return None
    
    from app.services.ai_service import AIService
    return AIService()


# =============================================================================
# Pagination Dependencies
# =============================================================================

class PaginationParams:
    """
    Common pagination parameters.
    """
    
    def __init__(
        self,
        page: int = 1,
        page_size: int = settings.DEFAULT_PAGE_SIZE,
    ):
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = settings.DEFAULT_PAGE_SIZE
        if page_size > settings.MAX_PAGE_SIZE:
            page_size = settings.MAX_PAGE_SIZE
        
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size
        self.limit = page_size


Pagination = Annotated[PaginationParams, Depends()]


# =============================================================================
# Sorting Dependencies
# =============================================================================

class SortParams:
    """
    Common sorting parameters.
    """
    
    def __init__(
        self,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ):
        self.sort_by = sort_by
        self.sort_order = sort_order.lower() if sort_order.lower() in ["asc", "desc"] else "asc"


Sorting = Annotated[SortParams, Depends()]


# =============================================================================
# Request Context Dependencies
# =============================================================================

async def get_request_id(
    x_request_id: Annotated[Optional[str], Header()] = None,
) -> str:
    """
    Get or generate request ID for tracing.
    """
    import uuid
    return x_request_id or str(uuid.uuid4())


RequestID = Annotated[str, Depends(get_request_id)]
