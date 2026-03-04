from datetime import datetime
from pydantic import BaseModel, Field
from src.models.enums import MediaType


class MediaSchema(BaseModel):
    media_url: str = Field(..., description="URL of the media file")
    media_type: MediaType = Field(
        ..., description="Type of the media file, incident photo or result sheet")

    model_config = {
        "from_attributes": True
    }
