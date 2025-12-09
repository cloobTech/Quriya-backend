from typing import TYPE_CHECKING
from sqlalchemy import JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import OrganizationType, SubscriptionTier, OrganizationStatus

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.election_project import ElectionProject


class Organization(BaseModel, Base):
    """ Organization Model """
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(nullable=False)
    contact_email: Mapped[str] = mapped_column(nullable=False)
    organization_type: Mapped[OrganizationType] = mapped_column(
        Enum(OrganizationType), nullable=True)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), nullable=True, default=SubscriptionTier.FREE_TRIAL)
    status: Mapped[OrganizationStatus] = mapped_column(
        Enum(OrganizationStatus), nullable=True)

    # Relationships
    users: Mapped[list['User']] = relationship(
        back_populates="organization", cascade="all, delete-orphan")
    election_projects: Mapped[list['ElectionProject']] = relationship(
        back_populates="organization", cascade="all, delete-orphan")
