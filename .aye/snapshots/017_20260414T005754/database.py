"""
Database Configuration
======================

SQLAlchemy async engine and session configuration.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings

# =============================================================================
# Async Engine
# =============================================================================

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Enable connection health checks
)

# For testing - use NullPool to avoid connection issues
test_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    poolclass=NullPool,
)

# =============================================================================
# Session Factory
# =============================================================================

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# =============================================================================
# Database Utilities
# =============================================================================

async def get_async_session() -> AsyncSession:
    """
    Get a new async database session.
    
    Use this for manual session management (e.g., in scripts).
    For FastAPI endpoints, use the get_db dependency.
    """
    async with async_session_factory() as session:
        return session


async def init_db() -> None:
    """
    Initialize database tables.
    
    Use Alembic migrations in production. This is for development/testing.
    """
    from app.models import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.
    """
    await engine.dispose()
