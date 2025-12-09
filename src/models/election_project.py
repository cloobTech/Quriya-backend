from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DATETIME, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus

if TYPE_CHECKING:
    from src.models.organization import Organization
    from src.models.election_project_member import ElectionProjectMember


class ElectionProject(BaseModel, Base):
    """Create a new monitoring project"""
    __tablename__ = "election_projects"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    election_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT)

    # Relationships
    organization: Mapped['Organization'] = relationship(
        back_populates="election_projects")
    members: Mapped[list['ElectionProjectMember']] = relationship(
        back_populates="project"
    )
