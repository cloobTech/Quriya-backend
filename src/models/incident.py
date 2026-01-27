from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import IncidentStatus, IncidentSeverity, IncidentType


if TYPE_CHECKING:
    from src.models.result import Result
    from src.models.media import ResultMedia


class Incident(BaseModel, Base):
    __tablename__ = "incidents"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), nullable=False)
    result_id: Mapped[str] = mapped_column(
        ForeignKey("results.id"), nullable=False
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN)
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity), nullable=False, default=IncidentSeverity.LOW
    )
    type: Mapped[IncidentType] = mapped_column(
        Enum(IncidentType), nullable=False, default=IncidentType.OTHER
    )

    result: Mapped['Result'] = relationship(back_populates="incidents")
    media_files: Mapped[list['ResultMedia']] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )
