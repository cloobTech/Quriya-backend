from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel, Base
from src.models.enums import MediaType


if TYPE_CHECKING:
    from src.models.result import Result


class ResultMedia(BaseModel, Base):
    """Model for storing media files associated with election results"""
    __tablename__ = "media"

    result_id: Mapped[str] = mapped_column(
        ForeignKey("results.id"), nullable=False)
    media_url: Mapped[str] = mapped_column(nullable=False)
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), nullable=False)

    # Relationships
    result: Mapped['Result'] = relationship(back_populates="media_files")
