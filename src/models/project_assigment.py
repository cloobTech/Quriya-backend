from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.project_member import ProjectMember


class ProjectAssignment(BaseModel, Base):
    """Assign Polling Unit to Projects Member
        - we could extend this to assign other entities in future
     """
    __tablename__ = "project_assignments"

    __table_args__ = (
        UniqueConstraint(
            "project_member_id",
            "polling_unit_id",
            name="uq_project_member_pu"
        ),
    )

    project_member_id: Mapped[str] = mapped_column(
        ForeignKey("project_members.id"), nullable=False
    )

    polling_unit_id: Mapped[str | None] = mapped_column(
        ForeignKey("polling_units.id"), nullable=True
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    member: Mapped['ProjectMember'] = relationship(
        back_populates="assignments"
    )
