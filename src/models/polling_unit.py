from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.ward import Ward


class PollingUnit(BaseModel, Base):
    """polling unit to be assigned to election project members"""

    __tablename__ = "polling_units"
    __table_args__ = (
        UniqueConstraint("ward_id", "name"),
    )

    ward_id: Mapped[str] = mapped_column(
        ForeignKey("wards.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    location_source: Mapped[str] = mapped_column(nullable=True)
    formatted_address: Mapped[str] = mapped_column(nullable=True)


    ward: Mapped["Ward"] = relationship(back_populates="polling_units")
