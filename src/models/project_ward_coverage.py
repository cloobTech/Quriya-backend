from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus


if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.ward import Ward
    from src.models.project_lga_coverage import ProjectLgaCoverage
    from src.models.project_pu_coverage import ProjectPuCoverage


class ProjectWardCoverage(BaseModel, Base):
    __tablename__ = "project_ward_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), primary_key=True)
    ward_id: Mapped[str] = mapped_column(
        ForeignKey("wards.id"), primary_key=True)
    lga_coverage_id: Mapped[str] = mapped_column(
        ForeignKey("project_lga_coverage.id"), nullable=False
    )

    status: Mapped[ElectionStatus] = mapped_column(
        Enum(ElectionStatus), default=ElectionStatus.DRAFT)

    project: Mapped["Project"] = relationship(back_populates="wards")
    ward: Mapped["Ward"] = relationship(uselist=False)
    lga_coverage: Mapped["ProjectLgaCoverage"] = relationship(
        uselist=False, back_populates="wards_coverage"
    )
    pu_coverage: Mapped["ProjectPuCoverage"] = relationship(
        uselist=False, back_populates="wards_coverage"
    )
