from pydantic import BaseModel
from typing import Any


class DefaultResponse(BaseModel):
    message: str
    data: Any  # Replace `Any` with a more specific schema if possible
