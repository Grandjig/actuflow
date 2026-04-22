#!/usr/bin/env python
"""Seed database with sample data."""

import asyncio
import sys
import os
from datetime import date, datetime, timedelta
from decimal import Decimal
import random
import uuid

# Ensure app is importable
sys.path.insert(0, '/app')

from sqlalchemy import select
from app.database import async_session_factory, init_db
from app.models.user import User
from app.models.role import Role, Permission
from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.models.claim import Claim
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.models.calculation_run import CalculationRun
from app.models.model_definition import ModelDefinition
from app.services.auth_service import get_password_hash


async def seed():
    """Seed the database."""
    print("Initializing database...")
    await init_db()
    
    async with async_session_factory() as db:
        # Check if already seeded
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print("Database already seeded. Skipping.")
            return
        
        print("Creating roles and permissions...")
        
        # Create permissions
        resources = ['policy', 'policyholder', 'claim', 'assumption', 'calculation', 'scenario', 'report', 'dashboard', 'import', 'user', 'role', 'automation', 'audit', 'document']
        actions = ['create', 'read', 'update', 'delete', 'approve', 'export']
        
        permissions = []
        for resource in resources:
            for action in actions:
                perm = Permission(resource=resource, action=action)
                permissions.append(perm)
                db.add(perm)
        
        await db.flush()
        
        # Create roles
        admin_role = Role(
            name="admin",
            description="Administrator with full access",
            permissions=permissions,
        )
        db.add(admin_role)
        
        actuary_perms = [p for p in permissions if p.resource in ['policy', 'policyholder', 'claim', 'assumption', 'calculation', 'scenario', 'report', 'dashboard'] and p.action in ['create', 'read', 'update']]
        actuary_role = Role(
            name="actuary",
            description="Actuary role",
            permissions=actuary_perms,
        )
        db.add(actuary_role)
        
        viewer_perms = [p for p in permissions if p.action == 'read']
        viewer_role = Role(
            name="viewer",
            description="Read-only access",
            permissions=viewer_perms,
        )
        db.add(viewer_role)
        
        await db.flush()
        
        print("Creating users...")
        
        # Create users
        admin_user = User(
            email="admin@actuflow.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            department="IT",
            is_active=True,
            is_superuser=True,
            role_id=admin_role.id,
        )
        db.add(admin_user)
        
        actuary_user = User(
            email="actuary@actuflow.com",
            hashed_password=get_password_hash("actuary123"),
            full_name="John Actuary",
            department="Actuarial",
            is_active=True,
            role_id=actuary_role.id,
        )
        db.add(actuary_user)
        
        viewer_user = User(
            email="viewer@actuflow.com",
            hashed_password=get_password_hash("viewer123"),
            full_name="Jane Viewer",
            department="Management",
            is_active=True,
            role_id=viewer_role.id,
        )
        db.add(viewer_user)
        
        await db.flush()
        
        print("Creating policyholders...")
        
        # Create policyholders
        policyholders = []
        names = [
            ("John", "Smith"), ("Jane", "Doe"), ("Robert", "Johnson"),
            ("Emily", "Williams"), ("Michael", "Brown"), ("Sarah", "Jones"),
            ("David", "Garcia"), ("Lisa", "Miller"), ("James", "Davis"),
            ("Mary", "Rodriguez"),
        ]
        
        for first, last in names:
            ph = Policyholder(
                first_name=first,
                last_name=last,
                date_of_birth=date(1970 + random.randint(0, 30), random.randint(1, 12), random.randint(1, 28)),
                gender=random.choice(["male", "female"]),
                smoker_status=random.choice(["non_smoker", "smoker"]),
                occupation_class=random.choice(["1", "2", "3", "4"]),
                email=f"{first.lower()}.{last.lower()}@email.com",
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            )
            policyholders.append(ph)
            db.add(ph)
        
        await db.flush()
        
        print("Creating model definition...")
        
        # Create a model definition first (required for calculation runs)
        model_def = ModelDefinition(
            name="Term Life Valuation Model",
            description="Standard term life insurance valuation model",
            model_type="valuation",
            line_of_business="life",
            regulatory_standard="IFRS17",
            configuration={
                "projection_months": 600,
                "discount_rate_source": "assumption_table",
            },
            version="1.0.0",
            status="active",
            created_by_id=actuary_user.id,
        )
        db.add(model_def)
        await db.flush()
        
        print("Creating assumption sets...")
        
        # Create assumption sets
        assumption_set = AssumptionSet(
            name="Base Assumptions 2024",
            version="1.0.0",
            description="Standard assumptions for 2024 valuations",
            status="approved",
            effective_date=date(2024, 1, 1),
            line_of_business="life",
            created_by_id=actuary_user.id,
            approved_by_id=admin_user.id,
            approval_date=datetime.utcnow(),
        )
        db.add(assumption_set)
        await db.flush()
        
        # Create assumption tables
        mortality_table = AssumptionTable(
            assumption_set_id=assumption_set.id,
            table_type="mortality",
            name="Base Mortality Table",
            description="SOA 2017 CSO mortality table",
            data={
                "ages": list(range(20, 100)),
                "male": [0.001 * (1.05 ** (age - 20)) for age in range(20, 100)],
                "female": [0.0008 * (1.05 ** (age - 20)) for age in range(20, 100)],
            },
        )
        db.add(mortality_table)
        
        lapse_table = AssumptionTable(
            assumption_set_id=assumption_set.id,
            table_type="lapse",
            name="Base Lapse Table",
            description="Historical lapse rates by policy year",
            data={
                "policy_years": list(range(1, 21)),
                "rates": [0.15, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02,
                          0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01],
            },
        )
        db.add(lapse_table)
        
        await db.flush()
        
        print("Creating policies...")
        
        # Create policies
        product_types = ["term_life", "whole_life", "universal_life", "endowment"]
        statuses = ["active", "active", "active", "active", "lapsed", "surrendered"]
        
        policies = []
        for i in range(50):
            product_type = random.choice(product_types)
            issue_date = date.today() - timedelta(days=random.randint(30, 3650))
            
            policy = Policy(
                policy_number=f"POL-2024-{str(i + 1).zfill(6)}",
                product_type=product_type,
                product_code=f"{product_type.upper()[:4]}-{random.randint(10, 30)}",
                product_name=f"{product_type.replace('_', ' ').title()} Plan",
                status=random.choice(statuses),
                policyholder_id=random.choice(policyholders).id,
                issue_date=issue_date,
                effective_date=issue_date,
                maturity_date=issue_date + timedelta(days=365 * random.randint(10, 30)),
                sum_assured=Decimal(random.choice([100000, 250000, 500000, 1000000])),
                premium_amount=Decimal(random.randint(500, 5000)),
                premium_frequency=random.choice(["monthly", "quarterly", "annual"]),
                currency="USD",
                risk_class=random.choice(["standard", "preferred", "substandard"]),
                branch_code="HQ",
            )
            policies.append(policy)
            db.add(policy)
        
        await db.flush()
        
        print("Creating claims...")
        
        # Create claims
        claim_types = ["death", "disability", "critical_illness", "hospitalization"]
        claim_statuses = ["filed", "under_review", "approved", "settled", "denied"]
        
        for i in range(20):
            policy = random.choice(policies)
            claim_date = date.today() - timedelta(days=random.randint(1, 365))
            claimed_amount = float(policy.sum_assured) * random.uniform(0.1, 1.0)
            status = random.choice(claim_statuses)
            
            claim = Claim(
                claim_number=f"CLM-2024-{str(i + 1).zfill(6)}",
                policy_id=policy.id,
                claim_type=random.choice(claim_types),
                status=status,
                claim_date=claim_date,
                incident_date=claim_date - timedelta(days=random.randint(1, 30)),
                claimed_amount=Decimal(claimed_amount),
                settlement_amount=Decimal(claimed_amount * 0.9) if status == "settled" else None,
                settlement_date=claim_date + timedelta(days=random.randint(30, 90)) if status == "settled" else None,
                anomaly_score=random.uniform(0, 1) if random.random() > 0.7 else None,
            )
            db.add(claim)
        
        await db.flush()
        
        print("Creating calculation runs...")
        
        # Create calculation runs
        for i in range(5):
            run_date = datetime.utcnow() - timedelta(days=i * 30)
            calc_run = CalculationRun(
                run_name=f"Monthly Valuation - {run_date.strftime('%B %Y')}",
                status="completed" if i > 0 else "running",
                trigger_type="manual",
                triggered_by_id=actuary_user.id,
                model_definition_id=model_def.id,
                assumption_set_id=assumption_set.id,
                started_at=run_date,
                completed_at=run_date + timedelta(minutes=random.randint(5, 30)) if i > 0 else None,
                duration_seconds=random.randint(300, 1800) if i > 0 else None,
                policies_count=50,
                result_summary={
                    "total_reserves": random.randint(10000000, 50000000),
                    "total_premiums": random.randint(1000000, 5000000),
                } if i > 0 else None,
            )
            db.add(calc_run)
        
        await db.commit()
        
        print("\n" + "="*50)
        print("\u2705 Database seeded successfully!")
        print("="*50)
        print("\nDefault users:")
        print("  admin@actuflow.com / admin123")
        print("  actuary@actuflow.com / actuary123")
        print("  viewer@actuflow.com / viewer123")
        print("\nSample data created:")
        print(f"  - {len(policyholders)} policyholders")
        print(f"  - {len(policies)} policies")
        print("  - 20 claims")
        print("  - 1 assumption set with mortality & lapse tables")
        print("  - 5 calculation runs")


if __name__ == "__main__":
    asyncio.run(seed())
