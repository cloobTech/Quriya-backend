from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus


if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.result import Result
    from src.models.project_assigment import ProjectAssignment
    from src.models.polling_unit import PollingUnit
    from src.models.project_ward_coverage import ProjectWardCoverage


class ProjectPuCoverage(BaseModel, Base):
    __tablename__ = "project_pu_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), primary_key=True)
    pu_id: Mapped[str] = mapped_column(
        ForeignKey("polling_units.id"), primary_key=True)
    ward_coverage_id: Mapped[str] = mapped_column(
        ForeignKey("project_ward_coverage.id"), nullable=False
    )
    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT, nullable=False)

    project: Mapped["Project"] = relationship(back_populates="polling_units")

    polling_units_results: Mapped[list["Result"]] = relationship(
        back_populates="polling_unit")
    assignments: Mapped[list["ProjectAssignment"]] = relationship(
        back_populates="pu_coverage")
    polling_unit: Mapped["PollingUnit"] = relationship(uselist=False)
    wards_coverage: Mapped[list["ProjectWardCoverage"]] = relationship(
        back_populates="pu_coverage")
