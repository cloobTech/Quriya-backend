from pydantic import BaseModel, Field
from src.models.enums import MediaType, IncidentSeverity, IncidentStatus, IncidentType


class MediaSchema(BaseModel):
    media_url: str = Field(..., description="URL of the media file")
    media_type: MediaType = Field(
        ..., description="Type of the media file, incident photo or result sheet")


class VotesSchema(BaseModel):
    party_id: str = Field(..., description="ID of the political party")
    valid_votes: int = Field(...,
                             description="Number of valid votes obtained by the party")


class IncidentSchema(BaseModel):
    description: str = Field(..., description="Description of the incident")
    severity: IncidentSeverity = Field(
        default=IncidentSeverity.LOW, description="Severity of the incident")
    type: IncidentType = Field(..., description="Type of the incident")
    status: IncidentStatus = Field(
        default=IncidentStatus.OPEN, description="Status of the incident")
    media: list[MediaSchema] = Field(
        default_factory=list, description="List of media files associated with the incident")


class SubmitResultSchema(BaseModel):
    pu_id: str = Field(..., description="ID of the processing unit")
    party_votes: list[VotesSchema] = Field(default_factory=list,
                                           description="Votes data submitted for the processing unit")
    total_votes_cast: int = Field(
        0, description="Total number of votes submitted")
    accredited_voters: int = Field(
        0, description="Total number of accredited voters")
    total_valid_votes: int = Field(
        0, description="Total number of valid votes")
    remarks: str | None = Field(
        None, description="Optional remarks for the result")
    total_invalid_votes: int = Field(
        0, description="Total number of invalid votes")
    total_cancelled_votes: int = Field(
        0, description="Total number of cancelled votes")
    media: list[MediaSchema] = Field(
        default_factory=list, description="List of media files associated with the result")
    incidents: list[IncidentSchema] = Field(
        default_factory=list, description="List of incidents associated with the result")
