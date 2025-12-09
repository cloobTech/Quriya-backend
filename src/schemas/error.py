from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    error: str = Field(...,
                       description="The type or code of the error that occurred.")
    message: str = Field(
        ..., description="A human-readable message providing more details about the error.")
    details: Optional[dict] = Field(
        default=None, description="Additional information about the error, if available.")
