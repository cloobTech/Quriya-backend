from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.project_member import ProjectMember
    from src.models.project_pu_coverage import ProjectPuCoverage


class ProjectAssignment(BaseModel, Base):
    """Assign Polling Unit to Projects Member
        - we could extend this to assign other entities in future
     """
    __tablename__ = "project_assignments"

    __table_args__ = (
        UniqueConstraint(
            "project_member_id",
            "pu_coverage_id",
            name="uq_project_member_pu"
        ),
    )

    project_member_id: Mapped[str] = mapped_column(
        ForeignKey("project_members.id"), nullable=False
    )

    pu_coverage_id: Mapped[str | None] = mapped_column(
        ForeignKey("project_pu_coverage.id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    member: Mapped['ProjectMember'] = relationship(
        back_populates="assignments"
    )

    pu_coverage: Mapped['ProjectPuCoverage'] = relationship(
        back_populates="assignments",
    )
