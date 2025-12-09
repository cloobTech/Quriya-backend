from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionRole, ElectionProjectMemberStatus

if TYPE_CHECKING:
    from src.models.election_project import ElectionProject
    from src.models.election_project_assigment import ElectionProjectAssignment


class ElectionProjectMember(BaseModel, Base):
    """his represents the person inside the context of the election project."""

    __tablename__ = "election_project_members"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    election_project_id: Mapped[str] = mapped_column(
        ForeignKey("election_projects.id"))
    role: Mapped[ElectionRole] = mapped_column(Enum(ElectionRole))
    status: Mapped[ElectionProjectMemberStatus] = mapped_column(Enum(ElectionProjectMemberStatus),
                                                                default=ElectionProjectMemberStatus.INVITED)

    project: Mapped['ElectionProject'] = relationship(
        back_populates="members"
    )
    assignments: Mapped[list['ElectionProjectAssignment']] = relationship(
        back_populates="member", cascade="all, delete-orphan"

    )
