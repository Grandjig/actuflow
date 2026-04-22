"""
Create Superuser Script
=======================

Creates a superuser account.

Usage:
    python -m scripts.create_superuser
"""

import asyncio
import getpass

from passlib.context import CryptContext
from sqlalchemy import select

from app.database import async_session_factory
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def main():
    print("\n👤 Create Superuser\n")
    
    email = input("Email: ").strip()
    if not email:
        print("Email is required")
        return
    
    full_name = input("Full name: ").strip()
    if not full_name:
        print("Full name is required")
        return
    
    password = getpass.getpass("Password: ")
    if len(password) < 8:
        print("Password must be at least 8 characters")
        return
    
    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords do not match")
        return
    
    async with async_session_factory() as db:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            print(f"User with email {email} already exists")
            return
        
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=pwd_context.hash(password),
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        
        print(f"\n✅ Superuser '{email}' created successfully!")


if __name__ == "__main__":
    asyncio.run(main())
