from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.party_vote import PartyVote
    from src.models.org_party_style import OrgPartyStyle
    from src.models.project_party_style import ProjectPartyStyle


class PoliticalParty(BaseModel, Base):
    __tablename__ = "political_parties"

    name: Mapped[str] = mapped_column(nullable=False)
    acronym: Mapped[str] = mapped_column(unique=True, nullable=False)
    logo_url: Mapped[str] = mapped_column(nullable=True)

    party_votes: Mapped[list['PartyVote']] = relationship(
        back_populates="party", cascade="all, delete-orphan"
    )

    org_party_style: Mapped[list['OrgPartyStyle']] = relationship(
        back_populates="political_party", cascade="all, delete-orphan"
    )

    project_party_style: Mapped[list['ProjectPartyStyle']] = relationship(
        back_populates="political_party", cascade="all, delete-orphan"
    )
