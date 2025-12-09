from pydantic import BaseModel, Field, computed_field
from typing import Optional
from src.models.enums import UserRole, UserStatus
from datetime import datetime


class CreateUser(BaseModel):
    first_name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")
    email: str = Field(..., description="The email address of the user")
    role: UserRole = Field(...,
                           description="The role of the user in the organization")
    status: UserStatus = Field(...,
                               description="The status of the user account")
    organization_id: Optional[str] = Field(
        None, description="The ID of the organization the user belongs to")
    password: Optional[str] = Field(None, description="user's plain password")
    admin_organization_id: Optional[str] = Field(
        None, description="ID of Admin carrying out the operation")

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserResponse(BaseModel):
    full_name: Optional[str] = Field(
        None, description="The full name of the user")
    first_name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")
    email: str = Field(..., description="The email address of the user")
    role: UserRole = Field(...,
                           description="The role of the user in the organization")
    status: UserStatus = Field(...,
                               description="The status of the user account")
    organization_id: Optional[str] = Field(
        None, description="The ID of the organization the user belongs to")
    created_at: datetime = Field(
        ..., description="The timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="The timestamp when the user was last updated")

    class Config:
        from_attributes = True
