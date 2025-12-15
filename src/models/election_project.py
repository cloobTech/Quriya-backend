from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DATETIME, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus, ElectionType

if TYPE_CHECKING:
    from src.models.organization import Organization
    from src.models.election_project_member import ElectionProjectMember
    from src.models.user import User
    from src.models.project_state_coverage import ProjectStateCoverage
    from src.models.project_lga_coverage import ProjectLgaCoverage
    from src.models.project_ward_coverage import ProjectWardCoverage
    from src.models.project_pu_coverage import ProjectPuCoverage


class ElectionProject(BaseModel, Base):
    """Create a new monitoring project"""
    __tablename__ = "election_projects"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=True)
    createdby_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    name: Mapped[str] = mapped_column(nullable=False)
    election_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT)
    election_type: Mapped[ElectionType] = mapped_column(Enum(ElectionType))


    # Relationships
    organization: Mapped['Organization'] = relationship(
        back_populates="election_projects")
    members: Mapped[list['ElectionProjectMember']] = relationship(
        back_populates="project"
    )

    created_by: Mapped['User'] = relationship(
        back_populates="election_project")

    # Georgraphical Coverage
    states: Mapped[list["ProjectStateCoverage"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    lgas: Mapped[list["ProjectLgaCoverage"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    wards: Mapped[list["ProjectWardCoverage"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    polling_units: Mapped[list["ProjectPuCoverage"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
