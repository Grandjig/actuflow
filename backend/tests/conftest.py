"""
Pytest configuration and fixtures for backend tests.
"""

import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.base import Base, get_db
from app.models import User, Role, Permission
from app.utils.security import hash_password
import uuid


# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db: Session) -> User:
    """Create an admin user for testing."""
    # Create admin role
    role = Role(
        id=str(uuid.uuid4()),
        name="admin",
        description="Administrator",
        is_system_role=True,
    )
    db.add(role)
    
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        email="admin@test.com",
        full_name="Test Admin",
        hashed_password=hash_password("admin123"),
        role_id=role.id,
        is_active=True,
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, admin_user: User) -> dict:
    """Get authentication headers for the admin user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def sample_policy_data() -> dict:
    """Sample policy data for testing."""
    return {
        "policy_number": "TEST-POL-001",
        "product_type": "term_life",
        "product_code": "TERM-20",
        "product_name": "20-Year Term Life",
        "status": "active",
        "issue_date": "2024-01-15",
        "effective_date": "2024-01-15",
        "sum_assured": 500000.00,
        "premium_amount": 1200.00,
        "premium_frequency": "annual",
        "currency": "USD",
    }


@pytest.fixture(scope="function")
def sample_assumption_set_data() -> dict:
    """Sample assumption set data for testing."""
    return {
        "name": "Test Assumption Set",
        "version": "1.0",
        "description": "Test assumptions for unit tests",
        "effective_date": "2024-01-01",
    }
