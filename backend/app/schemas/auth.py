"""
Auth Schemas
============

Schemas for authentication endpoints.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request body."""
    
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Token response after successful login."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token expiry in seconds")


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token."""
    
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Request password reset."""
    
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token."""
    
    token: str
    new_password: str = Field(min_length=8, max_length=128)
