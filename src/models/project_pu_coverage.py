
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ElectionStatus



if TYPE_CHECKING:
    from src.models.election_project import ElectionProject

class ProjectPuCoverage(BaseModel, Base):
    __tablename__ = "project_pu_coverage"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("election_projects.id"), primary_key=True)
    pu_id: Mapped[str] = mapped_column(
        ForeignKey("polling_units.id"), primary_key=True)
    status: Mapped[ElectionStatus] = mapped_column(Enum(ElectionStatus), nullable=False)
    
    

    project: Mapped["ElectionProject"] = relationship(back_populates="polling_units")
