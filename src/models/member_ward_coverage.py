from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.project_member import ProjectMember
    from src.models.project_ward_coverage import ProjectWardCoverage
    


class MemberWardCoverage(BaseModel, Base):
    """wards an agent may cover"""

    __tablename__ = "member_ward_coverage"

    __table_args__ = (
        UniqueConstraint(
            "member_id",
            "ward_coverage_id"
        ),
    )

    member_id: Mapped[str] = mapped_column(
        ForeignKey("project_members.id"), primary_key=True
    )
    ward_coverage_id: Mapped[str] = mapped_column(
        ForeignKey("project_ward_coverage.id"), nullable=True
    )

    member: Mapped['ProjectMember'] = relationship(
        back_populates="member_ward_coverage"
    )

    ward_coverage: Mapped['ProjectWardCoverage'] = relationship()
