from pydantic import BaseModel, Field
from datetime import datetime
from src.models.enums import ElectionStatus, ElectionType


class CreateElectionProject(BaseModel):
    """Create  a new election monitoring project"""

    name: str = Field(...,
                      description="The name of the project e.g. Kano Gubernutorial Election")
    election_date: datetime = Field(..., description="election date")
    status: ElectionStatus = Field(
        default=ElectionStatus.DRAFT, description="check if the execersie has been concluded, ")
    election_type: ElectionType

