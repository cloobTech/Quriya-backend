from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus


if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.project_member import ProjectMember
    from src.models.state import State
    from src.models.project_lga_coverage import ProjectLgaCoverage


class ProjectStateCoverage(BaseModel, Base):
    __tablename__ = "project_state_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), primary_key=True)
    state_id: Mapped[str] = mapped_column(
        ForeignKey("states.id"), primary_key=True)
    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT, nullable=False)

    project: Mapped["Project"] = relationship(back_populates="states")
    member: Mapped[list["ProjectMember"]] = relationship(
        back_populates="state_coverage")
    state: Mapped["State"] = relationship(uselist=False)
    lgas_coverage: Mapped[list["ProjectLgaCoverage"]] = relationship(
        back_populates="state_coverage")
