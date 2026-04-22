"""
Comment Model
=============

Comments/notes on any resource.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class Comment(Base, TimestampMixin, SoftDeleteMixin):
    """
    Comment on any resource.
    
    Supports threaded comments (replies) via parent_id.
    """
    
    __tablename__ = "comment"
    
    # Resource this comment is on
    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="policy/calculation_run/assumption_set/task/etc.",
    )
    
    resource_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    
    # Author
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Threading
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("comment.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    
    # Resolution (for review comments)
    is_resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    resolved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Mentions (user IDs mentioned in comment)
    mentions: Mapped[Optional[list]] = mapped_column(
        "mentions_json",
        nullable=True,
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    
    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side="Comment.id",
        foreign_keys=[parent_id],
        backref="replies",
    )
    
    resolved_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[resolved_by_id],
    )
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, resource={self.resource_type}/{self.resource_id})>"
