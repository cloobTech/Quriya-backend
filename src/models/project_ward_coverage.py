from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus



if TYPE_CHECKING:
    from src.models.election_project import ElectionProject


class ProjectWardCoverage(BaseModel, Base):
    __tablename__ = "project_ward_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("election_projects.id"), primary_key=True)
    ward_id: Mapped[str] = mapped_column(
        ForeignKey("wards.id"), primary_key=True)
    status: Mapped[ElectionStatus] = mapped_column(Enum(ElectionStatus))
    

    project: Mapped["ElectionProject"] = relationship(back_populates="wards")
