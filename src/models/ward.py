from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.polling_unit import PollingUnit
    from src.models.local_government_area import LGA


class Ward(BaseModel, Base):
    """Ward unit to be assigned to election project members"""

    __tablename__ = "wards"
    __table_args__ = (
        UniqueConstraint("lga_id", "name"),
    )

    lga_id: Mapped[str] = mapped_column(
        ForeignKey("local_government_areas.id"))
    name: Mapped[str] = mapped_column(nullable=False)

    lga: Mapped['LGA'] = relationship(back_populates="wards")
    polling_units: Mapped[list['PollingUnit']] = relationship(
        back_populates="ward"
    )
