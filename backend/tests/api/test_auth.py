"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_login_success(self, client: TestClient, admin_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient, admin_user):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@test.com", "password": "password123"}
        )
        assert response.status_code == 401

    def test_get_current_user(self, client: TestClient, auth_headers, admin_user):
        """Test getting current user info."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@test.com"
        assert data["full_name"] == "Test Admin"

    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_refresh_token(self, client: TestClient, admin_user):
        """Test refreshing access token."""
        # First login to get tokens
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "admin123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token to get new access token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_logout(self, client: TestClient, auth_headers):
        """Test logout."""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 200
