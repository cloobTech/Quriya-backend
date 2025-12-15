from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.ward import Ward
    from src.models.state import State


class LGA(BaseModel, Base):
    __tablename__ = "local_government_areas"
    __table_args__ = (UniqueConstraint("state_id", "name"),)

    state_id: Mapped[str] = mapped_column(ForeignKey("states.id"))
    name: Mapped[str] = mapped_column(nullable=False)

    state: Mapped["State"] = relationship(back_populates="lgas")
    wards: Mapped[list['Ward']] = relationship(back_populates="lga")
