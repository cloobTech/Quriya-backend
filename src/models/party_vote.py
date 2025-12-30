from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base

if TYPE_CHECKING:
    from src.models.result import Result
    from src.models.political_party import PoliticalParty


class PartyVote(BaseModel, Base):
    """Model for storing votes for political parties"""
    __tablename__ = "party_votes"

    result_id: Mapped[str] = mapped_column(
        ForeignKey("results.id"), nullable=False)
    party_id: Mapped[str] = mapped_column(
        ForeignKey("political_parties.id"), nullable=False)
    votes: Mapped[int] = mapped_column(nullable=False, default=0)

    # Relationships
    result: Mapped['Result'] = relationship(back_populates="party_votes")
    party: Mapped['PoliticalParty'] = relationship(
        back_populates="party_votes")
