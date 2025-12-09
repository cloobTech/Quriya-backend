from pydantic import BaseModel, Field
from datetime import datetime
from src.models.enums import ElectionStatus


class CreateElectionProject(BaseModel):
    """Create  a new election monitoring project"""
    organization_id: str = Field(
        ..., description="The ID of the organization creating the project")
    name: str = Field(...,
                      description="The name of the project e.g. Kano Gubernutorial Election")
    election_date: datetime = Field(..., description="election date")
    status: ElectionStatus = Field(default=ElectionStatus.DRAFT, description="check if the execersie has been concluded, ")
