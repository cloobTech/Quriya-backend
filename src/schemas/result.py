from datetime import datetime
from pydantic import BaseModel, Field
from src.schemas.media import MediaSchema


class VotesSchema(BaseModel):
    party_id: str = Field(..., description="ID of the political party")
    votes: int = Field(...,
                       description="Number of valid votes obtained by the party")

    model_config = {
        "from_attributes": True
    }


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

    model_config = {
        "from_attributes": True
    }


class ResultResponseSchema(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

    party_votes: list[VotesSchema] = []
    media_files: list[MediaSchema] = []

    total_votes_cast: int
    accredited_voters: int
    total_valid_votes: int
    total_invalid_votes: int
    total_cancelled_votes: int
    remarks: str | None

    model_config = {"from_attributes": True}
