from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.local_government_area import LGA


class State(BaseModel, Base):
    __tablename__ = "states"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    lgas: Mapped[list['LGA']] = relationship(back_populates='state')
