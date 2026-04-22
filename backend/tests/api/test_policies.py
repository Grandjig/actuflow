"""
Tests for policy endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Policy, Policyholder
import uuid


class TestPolicyEndpoints:
    """Test policy CRUD endpoints."""

    @pytest.fixture
    def policyholder(self, db: Session) -> Policyholder:
        """Create a test policyholder."""
        ph = Policyholder(
            id=str(uuid.uuid4()),
            first_name="John",
            last_name="Doe",
            date_of_birth="1980-01-15",
            gender="male",
            smoker_status="non_smoker",
        )
        db.add(ph)
        db.commit()
        db.refresh(ph)
        return ph

    def test_list_policies_empty(self, client: TestClient, auth_headers):
        """Test listing policies when none exist."""
        response = client.get("/api/v1/policies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_create_policy(
        self, 
        client: TestClient, 
        auth_headers, 
        sample_policy_data,
        policyholder
    ):
        """Test creating a new policy."""
        sample_policy_data["policyholder_id"] = policyholder.id
        
        response = client.post(
            "/api/v1/policies",
            json=sample_policy_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["policy_number"] == "TEST-POL-001"
        assert data["product_type"] == "term_life"
        assert data["status"] == "active"
        assert "id" in data

    def test_get_policy(
        self, 
        client: TestClient, 
        auth_headers, 
        db: Session,
        policyholder
    ):
        """Test getting a single policy."""
        # Create policy directly
        policy = Policy(
            id=str(uuid.uuid4()),
            policy_number="TEST-POL-002",
            product_type="term_life",
            product_code="TERM-20",
            status="active",
            policyholder_id=policyholder.id,
            issue_date="2024-01-15",
            effective_date="2024-01-15",
            sum_assured=500000,
            premium_amount=1200,
            premium_frequency="annual",
            currency="USD",
        )
        db.add(policy)
        db.commit()
        
        response = client.get(
            f"/api/v1/policies/{policy.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["policy_number"] == "TEST-POL-002"

    def test_get_policy_not_found(self, client: TestClient, auth_headers):
        """Test getting a non-existent policy."""
        fake_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/policies/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_policy(
        self, 
        client: TestClient, 
        auth_headers, 
        db: Session,
        policyholder
    ):
        """Test updating a policy."""
        # Create policy
        policy = Policy(
            id=str(uuid.uuid4()),
            policy_number="TEST-POL-003",
            product_type="term_life",
            product_code="TERM-20",
            status="active",
            policyholder_id=policyholder.id,
            issue_date="2024-01-15",
            effective_date="2024-01-15",
            sum_assured=500000,
            premium_amount=1200,
            premium_frequency="annual",
            currency="USD",
        )
        db.add(policy)
        db.commit()
        
        # Update policy
        response = client.put(
            f"/api/v1/policies/{policy.id}",
            json={"sum_assured": 750000},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sum_assured"] == 750000

    def test_delete_policy(
        self, 
        client: TestClient, 
        auth_headers, 
        db: Session,
        policyholder
    ):
        """Test deleting a policy (soft delete)."""
        # Create policy
        policy = Policy(
            id=str(uuid.uuid4()),
            policy_number="TEST-POL-004",
            product_type="term_life",
            product_code="TERM-20",
            status="active",
            policyholder_id=policyholder.id,
            issue_date="2024-01-15",
            effective_date="2024-01-15",
            sum_assured=500000,
            premium_amount=1200,
            premium_frequency="annual",
            currency="USD",
        )
        db.add(policy)
        db.commit()
        
        # Delete policy
        response = client.delete(
            f"/api/v1/policies/{policy.id}",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify it's no longer accessible
        response = client.get(
            f"/api/v1/policies/{policy.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_list_policies_with_filter(
        self, 
        client: TestClient, 
        auth_headers, 
        db: Session,
        policyholder
    ):
        """Test filtering policies."""
        # Create multiple policies
        for i, status in enumerate(["active", "active", "lapsed"]):
            policy = Policy(
                id=str(uuid.uuid4()),
                policy_number=f"TEST-POL-{i+10}",
                product_type="term_life",
                product_code="TERM-20",
                status=status,
                policyholder_id=policyholder.id,
                issue_date="2024-01-15",
                effective_date="2024-01-15",
                sum_assured=500000,
                premium_amount=1200,
                premium_frequency="annual",
                currency="USD",
            )
            db.add(policy)
        db.commit()
        
        # Filter by status
        response = client.get(
            "/api/v1/policies?status=active",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(p["status"] == "active" for p in data["items"])
