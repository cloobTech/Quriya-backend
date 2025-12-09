import uuid
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


class DomainEvent(BaseModel):
    """Base class for all domain events"""
    event_id: UUID = Field(default_factory=lambda: uuid4())
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = "DomainEvent"

    class Config:
        from_attributes = True
