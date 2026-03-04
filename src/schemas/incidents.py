from datetime import datetime
from pydantic import BaseModel, Field
from src.models.enums import IncidentSeverity, IncidentStatus, IncidentType
from src.schemas.media import MediaSchema


class IncidentSchema(BaseModel):
    description: str = Field(..., description="Description of the incident")
    severity: IncidentSeverity = Field(
        default=IncidentSeverity.LOW, description="Severity of the incident")
    type: IncidentType = Field(..., description="Type of the incident")
    status: IncidentStatus = Field(
        default=IncidentStatus.OPEN, description="Status of the incident")
    media_files: list[MediaSchema] = Field(
        default_factory=list, description="List of media files associated with the incident")

    model_config = {
        "from_attributes": True
    }
