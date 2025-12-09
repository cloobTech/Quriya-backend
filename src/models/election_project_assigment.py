from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.election_project_member import ElectionProjectMember
    from src.models.polling_unit import PollingUnit
    from src.models.ward import Ward


class ElectionProjectAssignment(BaseModel, Base):
    __tablename__ = "project_assignments"

    project_member_id: Mapped[str] = mapped_column(
        ForeignKey("election_project_members.id"), nullable=False
    )

    ward_id: Mapped[str | None] = mapped_column(
        ForeignKey("wards.id"), nullable=True
    )

    polling_unit_id: Mapped[str | None] = mapped_column(
        ForeignKey("polling_units.id"), nullable=True
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    member: Mapped['ElectionProjectMember'] = relationship(
        back_populates="assignments"
    )

    ward: Mapped['Ward'] = relationship()
    polling_unit: Mapped['PollingUnit'] = relationship()
