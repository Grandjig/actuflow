"""
Role and Permission Models
==========================

Role-based access control (RBAC) models.
"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


# Junction table for many-to-many relationship between Role and Permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permission.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Role(Base, TimestampMixin):
    """
    User role for access control.
    
    System roles cannot be deleted.
    """
    
    __tablename__ = "role"
    
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    # System roles cannot be deleted or modified
    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Relationships
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        lazy="dynamic",
    )
    
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="joined",
    )
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Check if role has a specific permission."""
        return any(
            p.resource == resource and p.action == action
            for p in self.permissions
        )


class Permission(Base):
    """
    Individual permission (resource + action combination).
    
    Examples:
    - resource="policy", action="create"
    - resource="calculation", action="run"
    - resource="assumption", action="approve"
    """
    
    __tablename__ = "permission"
    
    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
        lazy="dynamic",
    )
    
    def __repr__(self) -> str:
        return f"<Permission(resource={self.resource}, action={self.action})>"
    
    @property
    def name(self) -> str:
        """Permission name in format 'resource:action'."""
        return f"{self.resource}:{self.action}"
