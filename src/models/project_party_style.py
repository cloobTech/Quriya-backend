from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.political_party import PoliticalParty


class ProjectPartyStyle(BaseModel, Base):
    __tablename__ = "project_party_styles"
    __table_args__ = (UniqueConstraint("project_id", "political_party_id"),)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    political_party_id: Mapped[int] = mapped_column(
        ForeignKey("political_parties.id"))
    color: Mapped[str] = mapped_column(nullable=True)

    project: Mapped['Project'] = relationship(
        back_populates="project_party_style")
    political_party: Mapped['PoliticalParty'] = relationship(
        back_populates="project_party_style")
