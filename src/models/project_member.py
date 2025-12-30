from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionRole, ProjectMemberStatus

if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.project_assigment import ProjectAssignment


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
    role: Mapped[ElectionRole] = mapped_column(Enum(ElectionRole))
    status: Mapped[ProjectMemberStatus] = mapped_column(Enum(ProjectMemberStatus),
                                                        default=ProjectMemberStatus.INVITED)

    project: Mapped['Project'] = relationship(
        back_populates="members"
    )
    assignments: Mapped[list['ProjectAssignment']] = relationship(
        back_populates="member", cascade="all, delete-orphan"

    )
