"""Authentication API Routes."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dependencies import DBSession, CurrentUser
from app.services.auth_service import AuthService

router = APIRouter()


# =============================================================================
# Schemas
# =============================================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    department: str | None = None
    job_title: str | None = None
    is_active: bool
    is_superuser: bool
    role: dict | None = None
    last_login: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True


# =============================================================================
# Endpoints
# =============================================================================

@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: DBSession,
):
    """Authenticate user and return tokens."""
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(data.email, data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.flush()
    
    # Create tokens
    tokens = auth_service.create_tokens(user)
    
    return TokenResponse(**tokens)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    db: DBSession,
):
    """Refresh access token."""
    auth_service = AuthService(db)
    payload = auth_service.decode_token(data.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    user = await auth_service.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    tokens = auth_service.create_tokens(user)
    return TokenResponse(**tokens)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: CurrentUser,
):
    """Get current user profile."""
    role_data = None
    if current_user.role:
        role_data = {
            "id": str(current_user.role.id),
            "name": current_user.role.name,
            "description": current_user.role.description,
            "permissions": [
                f"{p.resource}:{p.action}" for p in current_user.role.permissions
            ] if current_user.role.permissions else [],
        }
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        department=current_user.department,
        job_title=current_user.job_title,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        role=role_data,
        last_login=current_user.last_login,
        created_at=current_user.created_at,
    )


@router.post("/logout")
async def logout(
    current_user: CurrentUser,
):
    """Logout current user."""
    # In a real implementation, you might want to blacklist the token
    # For now, just return success (client should discard the token)
    return {"message": "Logged out successfully"}
