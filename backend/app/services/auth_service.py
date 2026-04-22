"""Authentication Service."""

import uuid
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.user import User


def get_password_hash(password: str) -> str:
    """Hash a password using SHA-256 with salt.
    
    Note: For production, use bcrypt or argon2. This is a fallback
    due to bcrypt/passlib compatibility issues.
    """
    salt = secrets.token_hex(16)
    pw_hash = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${pw_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, pw_hash = hashed_password.split('$')
        check_hash = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
        return secrets.compare_digest(check_hash, pw_hash)
    except ValueError:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


class AuthService:
    """Authentication service."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return get_password_hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return verify_password(plain_password, hashed_password)
    
    def decode_token(self, token: str) -> Optional[dict]:
        """Decode token."""
        return decode_token(token)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email)
            .where(User.is_active == True)
            .where(User.is_deleted == False)
        )
        user = result.unique().scalar_one_or_none()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
            .where(User.is_active == True)
            .where(User.is_deleted == False)
        )
        return result.unique().scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email)
            .where(User.is_deleted == False)
        )
        return result.unique().scalar_one_or_none()
    
    def create_tokens(self, user: User) -> dict:
        """Create access and refresh tokens for user."""
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
