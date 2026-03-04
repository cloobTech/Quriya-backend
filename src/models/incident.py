from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import IncidentStatus, IncidentSeverity, IncidentType


if TYPE_CHECKING:
    from src.models.media import ResultMedia
    from src.models.project_pu_coverage import ProjectPuCoverage


class Incident(BaseModel, Base):
    __tablename__ = "incidents"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), nullable=False)
    polling_unit_id: Mapped[str] = mapped_column(
        ForeignKey("project_pu_coverage.id"), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN)
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity), nullable=False, default=IncidentSeverity.LOW
    )
    type: Mapped[IncidentType] = mapped_column(
        Enum(IncidentType), nullable=False, default=IncidentType.OTHER
    )

    media_files: Mapped[list['ResultMedia']] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )
    polling_unit: Mapped['ProjectPuCoverage'] = relationship(
        back_populates="incidents")
