from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.ward import Ward


class PollingUnit(BaseModel, Base):
    """polling unit to be assigned to election project members"""

    __tablename__ = "polling_units"

    ward_id: Mapped[str] = mapped_column(
        ForeignKey("wards.id"), nullable=False)
    name: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column()

    ward: Mapped["Ward"] = relationship("Ward", back_populates="polling_units")
