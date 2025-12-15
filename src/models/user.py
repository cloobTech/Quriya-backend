from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import UserRole, UserStatus


if TYPE_CHECKING:
    from src.models.organization import Organization
    from src.models.election_project import ElectionProject


class User(BaseModel, Base):
    """ User Model """
    __tablename__ = "users"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.STAFF)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), nullable=False, default=UserStatus.PENDING_ACTIVATION)
    token: Mapped[str] = mapped_column(nullable=True)
    last_login: Mapped[datetime] = mapped_column(DATETIME, nullable=True)

    # Relationships
    organization: Mapped['Organization'] = relationship(
        back_populates="users")
    election_project: Mapped['ElectionProject'] = relationship(
        back_populates="created_by")
