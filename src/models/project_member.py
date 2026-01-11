from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionRole, ProjectMemberStatus
from src.models.user import User

if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.project_assigment import ProjectAssignment
    from src.models.project_state_coverage import ProjectStateCoverage
    from src.models.project_lga_coverage import ProjectLgaCoverage
    from src.models.project_ward_coverage import ProjectWardCoverage
    from src.models.member_ward_coverage import MemberWardCoverage


class ProjectMember(BaseModel, Base):
    """his represents the person inside the context of the election project."""

    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint(
            "election_project_id",
            "user_id",
            name="uq_project_member"
        ),
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    election_project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"))
    state_coverage_id: Mapped[str] = mapped_column(
        ForeignKey("project_state_coverage.id"), nullable=True
    )
    lga_coverage_id: Mapped[str] = mapped_column(
        ForeignKey("project_lga_coverage.id"), nullable=True
    )

    role: Mapped[ElectionRole] = mapped_column(
        Enum(ElectionRole), default=ElectionRole.FIELD_AGENT)
    status: Mapped[ProjectMemberStatus] = mapped_column(Enum(ProjectMemberStatus),
                                                        default=ProjectMemberStatus.INVITED)

    project: Mapped['Project'] = relationship(
        back_populates="members"
    )
    assignments: Mapped[list['ProjectAssignment']] = relationship(

        back_populates="member", cascade="all, delete-orphan"

    )

    user: Mapped['User'] = relationship(
        back_populates="member"
    )


    state_coverage: Mapped["ProjectStateCoverage"] = relationship(
        back_populates="member"
    )

    lga_coverage: Mapped["ProjectLgaCoverage"] = relationship(
        back_populates="member"
    )

    member_ward_coverage: Mapped[list["MemberWardCoverage"] ]= relationship(
        back_populates="member"
    )