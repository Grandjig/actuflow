"""Database Seeding Script.

Creates sample data for development and testing.
"""

import asyncio
import uuid
from datetime import date, datetime, timedelta
import random

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import models
import sys
sys.path.insert(0, '.')

from app.config import settings
from app.models import Base
from app.models.user import User
from app.models.role import Role, Permission
from app.models.policy import Policy
from app.models.policyholder import Policyholder
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.models.model_definition import ModelDefinition
from app.utils.security import get_password_hash


async def seed_database():
    """Seed the database with sample data."""
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("Seeding database...")

        # Create permissions
        permissions = []
        resources = ['policy', 'policyholder', 'claim', 'assumption', 'model',
                     'calculation', 'scenario', 'report', 'dashboard', 'import',
                     'task', 'user', 'role', 'automation', 'audit', 'ai']
        actions = ['create', 'read', 'update', 'delete', 'approve', 'export']

        for resource in resources:
            for action in actions:
                perm = Permission(
                    resource=resource,
                    action=action,
                    description=f"{action.title()} {resource}"
                )
                permissions.append(perm)
                session.add(perm)

        await session.flush()
        print(f"Created {len(permissions)} permissions")

        # Create roles
        admin_role = Role(
            name="Administrator",
            description="Full system access",
            is_system=True,
        )
        admin_role.permissions = permissions
        session.add(admin_role)

        actuary_role = Role(
            name="Actuary",
            description="Standard actuarial user",
            is_system=True,
        )
        actuary_perms = [p for p in permissions if p.action in ['create', 'read', 'update']]
        actuary_role.permissions = actuary_perms
        session.add(actuary_role)

        viewer_role = Role(
            name="Viewer",
            description="Read-only access",
            is_system=True,
        )
        viewer_perms = [p for p in permissions if p.action == 'read']
        viewer_role.permissions = viewer_perms
        session.add(viewer_role)

        await session.flush()
        print("Created roles")

        # Create users
        admin_user = User(
            email="admin@actuflow.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role=admin_role,
            is_active=True,
            is_superuser=True,
        )
        session.add(admin_user)

        actuary_user = User(
            email="actuary@actuflow.com",
            full_name="Jane Actuary",
            hashed_password=get_password_hash("actuary123"),
            role=actuary_role,
            department="Actuarial",
            job_title="Senior Actuary",
            is_active=True,
        )
        session.add(actuary_user)

        viewer_user = User(
            email="viewer@actuflow.com",
            full_name="Bob Viewer",
            hashed_password=get_password_hash("viewer123"),
            role=viewer_role,
            is_active=True,
        )
        session.add(viewer_user)

        await session.flush()
        print("Created users")

        # Create policyholders
        policyholders = []
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

        for i in range(50):
            ph = Policyholder(
                external_id=f"PH-{10000 + i}",
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                date_of_birth=date(1960 + random.randint(0, 40), random.randint(1, 12), random.randint(1, 28)),
                gender=random.choice(["male", "female"]),
                smoker_status=random.choice(["non_smoker", "smoker", "ex_smoker"]),
                occupation_class=random.choice(["1", "2", "3", "4"]),
                email=f"policyholder{i}@example.com",
                city=random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
                state=random.choice(["NY", "CA", "IL", "TX", "AZ"]),
                country="USA",
                created_by_id=admin_user.id,
            )
            policyholders.append(ph)
            session.add(ph)

        await session.flush()
        print(f"Created {len(policyholders)} policyholders")

        # Create policies
        product_types = ["term_life", "whole_life", "universal_life", "endowment"]
        statuses = ["active", "active", "active", "active", "lapsed", "surrendered"]

        for i in range(200):
            product_type = random.choice(product_types)
            ph = random.choice(policyholders)

            policy = Policy(
                policy_number=f"POL-{2024}-{100000 + i}",
                product_type=product_type,
                product_code=f"{product_type.upper()[:4]}-{random.randint(10, 30)}",
                product_name=f"{product_type.replace('_', ' ').title()} Insurance",
                status=random.choice(statuses),
                policyholder_id=ph.id,
                issue_date=date(2020 + random.randint(0, 4), random.randint(1, 12), random.randint(1, 28)),
                effective_date=date(2020 + random.randint(0, 4), random.randint(1, 12), random.randint(1, 28)),
                maturity_date=date(2040 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                sum_assured=random.choice([50000, 100000, 250000, 500000, 1000000]),
                premium_amount=random.randint(100, 2000),
                premium_frequency=random.choice(["monthly", "quarterly", "annual"]),
                currency="USD",
                risk_class=random.choice(["standard", "preferred", "substandard"]),
                created_by_id=admin_user.id,
            )
            session.add(policy)

        await session.flush()
        print("Created 200 policies")

        # Create assumption set
        assumption_set = AssumptionSet(
            name="Base Assumptions 2024",
            version="1.0.0",
            description="Standard assumptions for 2024 valuations",
            status="approved",
            effective_date=date(2024, 1, 1),
            approved_by_id=admin_user.id,
            approval_date=datetime.utcnow(),
            created_by_id=admin_user.id,
        )
        session.add(assumption_set)
        await session.flush()

        # Create assumption tables
        mortality_table = AssumptionTable(
            assumption_set_id=assumption_set.id,
            table_type="mortality",
            name="Standard Mortality Table",
            description="Select and ultimate mortality rates",
            data={
                "type": "select_ultimate",
                "select_period": 15,
                "rates": [
                    {"age": age, "duration": 1, "male": 0.0005 * (1 + age/100), "female": 0.0003 * (1 + age/100)}
                    for age in range(20, 80)
                ]
            }
        )
        session.add(mortality_table)

        lapse_table = AssumptionTable(
            assumption_set_id=assumption_set.id,
            table_type="lapse",
            name="Standard Lapse Rates",
            description="Policy lapse rates by duration",
            data={
                "rates": [
                    {"duration": 1, "rate": 0.10},
                    {"duration": 2, "rate": 0.08},
                    {"duration": 3, "rate": 0.06},
                    {"duration": 4, "rate": 0.05},
                    {"duration": 5, "rate": 0.04},
                    {"duration": 10, "rate": 0.03},
                    {"duration": 15, "rate": 0.02},
                ]
            }
        )
        session.add(lapse_table)

        discount_table = AssumptionTable(
            assumption_set_id=assumption_set.id,
            table_type="discount_rate",
            name="Discount Curve",
            description="Risk-free discount rates",
            data={
                "rates": [
                    {"term_months": 12, "rate": 0.04},
                    {"term_months": 60, "rate": 0.045},
                    {"term_months": 120, "rate": 0.05},
                    {"term_months": 240, "rate": 0.055},
                    {"term_months": 360, "rate": 0.055},
                ]
            }
        )
        session.add(discount_table)

        await session.flush()
        print("Created assumption set with tables")

        # Create model definition
        model = ModelDefinition(
            name="Standard Reserve Model",
            description="Standard term life reserve calculation model",
            model_type="reserving",
            line_of_business="term_life",
            version="1.0.0",
            status="active",
            configuration={
                "projection_months": 360,
                "time_step": "monthly",
                "nodes": [
                    {"id": "policy_data", "type": "input", "source": "policy"},
                    {"id": "mortality", "type": "table_lookup", "table_type": "mortality"},
                    {"id": "lapse", "type": "table_lookup", "table_type": "lapse"},
                    {"id": "discount", "type": "table_lookup", "table_type": "discount_rate"},
                    {"id": "reserve", "type": "calculation", "formula": "pv_benefits - pv_premiums"},
                ],
                "outputs": ["reserve", "cashflows"]
            },
            created_by_id=admin_user.id,
        )
        session.add(model)

        await session.commit()
        print("Database seeding completed!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
