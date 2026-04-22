"""
Database Seeding Script
=======================

Populates the database with sample data for development/testing.

Usage:
    python -m scripts.seed_db
"""

import asyncio
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
import random

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory, engine
from app.models import Base
from app.models.user import User
from app.models.role import Role, Permission
from app.models.policyholder import Policyholder
from app.models.policy import Policy
from app.models.coverage import Coverage
from app.models.claim import Claim
from app.models.assumption_set import AssumptionSet
from app.models.assumption_table import AssumptionTable
from app.models.model_definition import ModelDefinition

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_tables():
    """Create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created")


async def seed_permissions(db: AsyncSession) -> list[Permission]:
    """Seed permissions."""
    resources = [
        "policy", "policyholder", "claim", "assumption", "model",
        "calculation", "scenario", "report", "dashboard", "import",
        "task", "user", "role", "automation", "audit", "ai", "document"
    ]
    actions = ["create", "read", "update", "delete", "approve", "export"]
    
    permissions = []
    for resource in resources:
        for action in actions:
            perm = Permission(
                resource=resource,
                action=action,
                description=f"{action.title()} {resource}",
            )
            db.add(perm)
            permissions.append(perm)
    
    await db.flush()
    print(f"✓ Created {len(permissions)} permissions")
    return permissions


async def seed_roles(db: AsyncSession, permissions: list[Permission]) -> dict[str, Role]:
    """Seed roles."""
    all_permissions = permissions
    read_permissions = [p for p in permissions if p.action == "read"]
    actuary_permissions = [
        p for p in permissions 
        if p.resource in ["policy", "policyholder", "claim", "assumption", "model", "calculation", "scenario", "report", "dashboard", "task", "ai"]
    ]
    
    roles = {
        "admin": Role(
            name="Administrator",
            description="Full system access",
            is_system=True,
            permissions=all_permissions,
        ),
        "actuary": Role(
            name="Actuary",
            description="Actuarial team member",
            is_system=True,
            permissions=actuary_permissions,
        ),
        "viewer": Role(
            name="Viewer",
            description="Read-only access",
            is_system=True,
            permissions=read_permissions,
        ),
    }
    
    for role in roles.values():
        db.add(role)
    
    await db.flush()
    print(f"✓ Created {len(roles)} roles")
    return roles


async def seed_users(db: AsyncSession, roles: dict[str, Role]) -> list[User]:
    """Seed users."""
    users = [
        User(
            email="admin@actuflow.com",
            full_name="System Administrator",
            hashed_password=pwd_context.hash("admin123"),
            department="IT",
            is_active=True,
            is_superuser=True,
            role_id=roles["admin"].id,
        ),
        User(
            email="actuary@actuflow.com",
            full_name="John Smith",
            hashed_password=pwd_context.hash("actuary123"),
            department="Actuarial",
            is_active=True,
            is_superuser=False,
            role_id=roles["actuary"].id,
        ),
        User(
            email="viewer@actuflow.com",
            full_name="Jane Doe",
            hashed_password=pwd_context.hash("viewer123"),
            department="Finance",
            is_active=True,
            is_superuser=False,
            role_id=roles["viewer"].id,
        ),
    ]
    
    for user in users:
        db.add(user)
    
    await db.flush()
    print(f"✓ Created {len(users)} users")
    return users


async def seed_policyholders(db: AsyncSession) -> list[Policyholder]:
    """Seed policyholders."""
    first_names = ["James", "Mary", "Robert", "Patricia", "Michael", "Jennifer", "William", "Linda", "David", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    policyholders = []
    for i in range(50):
        birth_year = random.randint(1950, 2000)
        ph = Policyholder(
            external_id=f"PH-{i+1:05d}",
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            date_of_birth=date(birth_year, random.randint(1, 12), random.randint(1, 28)),
            gender=random.choice(["male", "female"]),
            smoker_status=random.choice(["non_smoker", "non_smoker", "non_smoker", "smoker"]),
            occupation_class=random.choice(["1", "2", "3", "4"]),
            email=f"policyholder{i+1}@example.com",
            city=random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            state=random.choice(["NY", "CA", "IL", "TX", "AZ"]),
            country="USA",
        )
        db.add(ph)
        policyholders.append(ph)
    
    await db.flush()
    print(f"✓ Created {len(policyholders)} policyholders")
    return policyholders


async def seed_policies(db: AsyncSession, policyholders: list[Policyholder]) -> list[Policy]:
    """Seed policies."""
    product_types = ["term_life", "whole_life", "universal_life", "endowment"]
    product_codes = ["TERM-20", "TERM-30", "WL-100", "UL-FLEX", "END-20"]
    
    policies = []
    for i, ph in enumerate(policyholders):
        # Each policyholder gets 1-3 policies
        num_policies = random.randint(1, 3)
        for j in range(num_policies):
            issue_date = date.today() - timedelta(days=random.randint(30, 3650))
            sum_assured = Decimal(random.choice([100000, 250000, 500000, 1000000]))
            premium = sum_assured * Decimal("0.002") * Decimal(random.randint(8, 15)) / 10
            
            policy = Policy(
                policy_number=f"POL-{len(policies)+1:06d}",
                product_type=random.choice(product_types),
                product_code=random.choice(product_codes),
                product_name=f"Sample {random.choice(['Life', 'Protection', 'Security'])} Plan",
                status=random.choice(["active", "active", "active", "lapsed", "surrendered"]),
                policyholder_id=ph.id,
                issue_date=issue_date,
                effective_date=issue_date,
                maturity_date=issue_date + timedelta(days=365*20),
                sum_assured=sum_assured,
                premium_amount=round(premium, 2),
                premium_frequency=random.choice(["monthly", "annual", "quarterly"]),
                currency="USD",
                branch_code=random.choice(["NYC", "LA", "CHI", "HOU"]),
            )
            db.add(policy)
            policies.append(policy)
    
    await db.flush()
    print(f"✓ Created {len(policies)} policies")
    return policies


async def seed_claims(db: AsyncSession, policies: list[Policy]) -> list[Claim]:
    """Seed claims."""
    claims = []
    claim_types = ["death", "disability", "hospitalization", "accident"]
    
    # ~10% of policies have claims
    for policy in random.sample(policies, len(policies) // 10):
        claim_date = date.today() - timedelta(days=random.randint(1, 365))
        claimed_amount = policy.sum_assured * Decimal(random.choice([0.1, 0.25, 0.5, 1.0]))
        
        claim = Claim(
            claim_number=f"CLM-{len(claims)+1:06d}",
            policy_id=policy.id,
            claim_date=claim_date,
            incident_date=claim_date - timedelta(days=random.randint(1, 30)),
            claim_type=random.choice(claim_types),
            claimed_amount=round(claimed_amount, 2),
            status=random.choice(["submitted", "under_review", "approved", "paid", "denied"]),
            anomaly_score=random.random() if random.random() < 0.1 else None,
        )
        db.add(claim)
        claims.append(claim)
    
    await db.flush()
    print(f"✓ Created {len(claims)} claims")
    return claims


async def seed_assumptions(db: AsyncSession, users: list[User]) -> list[AssumptionSet]:
    """Seed assumption sets."""
    admin_user = users[0]
    
    assumption_sets = []
    for i, (name, status) in enumerate([
        ("2024 Q1 Assumptions", "approved"),
        ("2024 Q2 Assumptions", "approved"),
        ("2024 Q3 Assumptions", "pending_approval"),
        ("2024 Q4 Assumptions (Draft)", "draft"),
    ]):
        aset = AssumptionSet(
            name=name,
            version=f"1.{i}",
            description=f"Assumption set for {name}",
            status=status,
            effective_date=date(2024, (i+1)*3, 1),
            created_by_id=admin_user.id,
            approved_by_id=admin_user.id if status == "approved" else None,
            approval_date=datetime.utcnow() if status == "approved" else None,
        )
        db.add(aset)
        assumption_sets.append(aset)
    
    await db.flush()
    
    # Add tables to each set
    table_types = ["mortality", "lapse", "expense", "discount_rate"]
    for aset in assumption_sets:
        for table_type in table_types:
            table = AssumptionTable(
                assumption_set_id=aset.id,
                table_type=table_type,
                name=f"{table_type.title()} Table",
                description=f"Standard {table_type} assumptions",
                data={"rates": {str(age): round(0.001 * age, 4) for age in range(20, 100, 5)}},
            )
            db.add(table)
    
    await db.flush()
    print(f"✓ Created {len(assumption_sets)} assumption sets with tables")
    return assumption_sets


async def seed_models(db: AsyncSession, users: list[User]) -> list[ModelDefinition]:
    """Seed model definitions."""
    admin_user = users[0]
    
    models = [
        ModelDefinition(
            name="Standard Reserve Model",
            description="IFRS17 compliant reserve calculation model",
            model_type="reserving",
            line_of_business="life",
            regulatory_standard="IFRS17",
            configuration={"method": "BEL", "risk_adjustment": 0.05},
            version="1.0.0",
            status="active",
            is_system_model=True,
            created_by_id=admin_user.id,
        ),
        ModelDefinition(
            name="Cash Flow Projection Model",
            description="Monthly cash flow projections",
            model_type="cashflow",
            line_of_business="life",
            configuration={"projection_months": 600, "stochastic": False},
            version="1.0.0",
            status="active",
            is_system_model=True,
            created_by_id=admin_user.id,
        ),
    ]
    
    for model in models:
        db.add(model)
    
    await db.flush()
    print(f"✓ Created {len(models)} model definitions")
    return models


async def main():
    """Main seeding function."""
    print("\n🌱 Starting database seed...\n")
    
    await create_tables()
    
    async with async_session_factory() as db:
        try:
            # Check if already seeded
            result = await db.execute(select(User).limit(1))
            if result.scalar_one_or_none():
                print("⚠️  Database already has data. Skipping seed.")
                print("   To reseed, run: make db-reset && make seed")
                return
            
            permissions = await seed_permissions(db)
            roles = await seed_roles(db, permissions)
            users = await seed_users(db, roles)
            policyholders = await seed_policyholders(db)
            policies = await seed_policies(db, policyholders)
            claims = await seed_claims(db, policies)
            assumptions = await seed_assumptions(db, users)
            models = await seed_models(db, users)
            
            await db.commit()
            print("\n✅ Database seeding complete!")
            print("\n📝 Login credentials:")
            print("   Admin:   admin@actuflow.com / admin123")
            print("   Actuary: actuary@actuflow.com / actuary123")
            print("   Viewer:  viewer@actuflow.com / viewer123")
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ Seeding failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
