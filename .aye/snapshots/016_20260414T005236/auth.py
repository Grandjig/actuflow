"""
Authentication API Routes
=========================

Login, logout, token refresh, and password management.
"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.dependencies import CurrentUser, DBSession, get_current_user
from app.schemas.auth import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.user import UserProfile, UserPasswordChange

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession,
    request: Request,
):
    """
    Authenticate user and return JWT tokens.
    
    Accepts standard OAuth2 form data (username/password).
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    
    # Authenticate user
    user = await auth_service.authenticate(
        email=form_data.username,
        password=form_data.password,
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )
    
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please try again later.",
        )
    
    # Generate tokens
    tokens = await auth_service.create_tokens(user)
    
    # Update last login
    await auth_service.record_login(
        user=user,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: DBSession,
):
    """
    Refresh access token using refresh token.
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    
    tokens = await auth_service.refresh_tokens(request.refresh_token)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    return tokens


@router.post("/logout")
async def logout(
    user: CurrentUser,
    db: DBSession,
):
    """
    Logout current user (invalidate tokens).
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    await auth_service.logout(user)
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    user: CurrentUser,
):
    """
    Get current authenticated user's profile.
    """
    return user


@router.put("/me/password")
async def change_password(
    password_data: UserPasswordChange,
    user: CurrentUser,
    db: DBSession,
):
    """
    Change current user's password.
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    
    success = await auth_service.change_password(
        user=user,
        current_password=password_data.current_password,
        new_password=password_data.new_password,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    
    return {"message": "Password changed successfully"}


@router.post("/password-reset/request")
async def request_password_reset(
    request: PasswordResetRequest,
    db: DBSession,
):
    """
    Request a password reset email.
    
    Always returns success to prevent email enumeration.
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    await auth_service.request_password_reset(request.email)
    
    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/password-reset/confirm")
async def confirm_password_reset(
    request: PasswordResetConfirm,
    db: DBSession,
):
    """
    Confirm password reset with token.
    """
    from app.services.auth_service import AuthService
    
    auth_service = AuthService(db)
    
    success = await auth_service.reset_password(
        token=request.token,
        new_password=request.new_password,
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    
    return {"message": "Password has been reset successfully"}
