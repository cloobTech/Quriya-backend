from pydantic import BaseModel
from typing import Literal

class CreateAdminSchema(BaseModel):
    """Admin schema"""
    full_name: str
    preferred_location: str
    