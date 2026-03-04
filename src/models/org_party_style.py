from typing import TYPE_CHECKING
from src.models.base import BaseModel, Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base


if TYPE_CHECKING:
    from src.models.organization import Organization
    from src.models.political_party import PoliticalParty


class OrgPartyStyle(BaseModel, Base):
    __tablename__ = "org_party_styles"
    __table_args__ = (UniqueConstraint("organization_id", "political_party_id"),)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    political_party_id: Mapped[int] = mapped_column(ForeignKey("political_parties.id"))
    color: Mapped[str] = mapped_column(nullable=True)


    organization: Mapped['Organization'] = relationship(back_populates="org_party_style")
    political_party: Mapped['PoliticalParty'] = relationship(back_populates="org_party_style")