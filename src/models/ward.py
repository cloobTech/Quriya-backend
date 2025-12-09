from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.polling_unit import PollingUnit


class Ward(BaseModel, Base):
    """Ward unit to be assigned to election project members"""

    __tablename__ = "wards"
    
    name: Mapped[str] = mapped_column()
    lga_id: Mapped[str] = mapped_column()

    polling_units: Mapped[list['PollingUnit']] = relationship(
        back_populates="ward"
    )
