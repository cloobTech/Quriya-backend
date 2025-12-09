from src.events.base import DomainEvent
from pydantic import Field
from datetime import datetime


class OrganizationCreatedEvent(DomainEvent):
    admin_name: str
    organization_name: str
    admin_email: str
    year: int = Field(default_factory=lambda: datetime.now().year, description="The year the organization was created")