from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus


if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.project_member import ProjectMember
    from src.models.local_government_area import LGA



class ProjectLgaCoverage(BaseModel, Base):
    __tablename__ = "project_lga_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), primary_key=True)
    lga_id: Mapped[str] = mapped_column(ForeignKey(
        "local_government_areas.id"), primary_key=True)
    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT, nullable=False)

    project: Mapped["Project"] = relationship(back_populates="lgas")
    member: Mapped["ProjectMember"] = relationship(
        back_populates="lga_coverage")
    lga: Mapped["LGA"] = relationship(uselist=False)

