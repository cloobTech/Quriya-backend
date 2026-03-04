from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import ResultStatus

if TYPE_CHECKING:
    from src.models.project import Project
    from src.models.user import User
    from src.models.media import ResultMedia
    from src.models.party_vote import PartyVote
    from src.models.project_pu_coverage import ProjectPuCoverage


class Result(BaseModel, Base):
    """Model for storing election results"""
    __tablename__ = "results"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id"), nullable=False)
    polling_unit_id: Mapped[str] = mapped_column(
        ForeignKey("project_pu_coverage.id"), nullable=False)
    submitted_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    verified_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    accredited_voters: Mapped[int] = mapped_column(nullable=False, default=0)
    total_votes_cast: Mapped[int] = mapped_column(nullable=False, default=0)
    total_valid_votes: Mapped[int] = mapped_column(nullable=False, default=0)
    total_invalid_votes: Mapped[int] = mapped_column(nullable=False, default=0)
    total_cancelled_votes: Mapped[int] = mapped_column(
        nullable=False, default=0)
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ResultStatus] = mapped_column(
        Enum(ResultStatus), default=ResultStatus.PENDING_REVIEW)

    # Relationships
    project: Mapped['Project'] = relationship(back_populates="results")
    polling_unit: Mapped['ProjectPuCoverage'] = relationship(
        back_populates="polling_units_result")
    submitted_by: Mapped['User'] = relationship(
        foreign_keys=[submitted_by_user_id], back_populates="submitted_results")
    verified_by: Mapped['User'] = relationship(
        foreign_keys=[verified_by_user_id], back_populates="verified_results")

    media_files: Mapped[list['ResultMedia']] = relationship(
        back_populates="result", cascade="all, delete-orphan"
    )
    party_votes: Mapped[list['PartyVote']] = relationship(
        back_populates="result", cascade="all, delete-orphan"
    )
