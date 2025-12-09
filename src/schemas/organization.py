from pydantic import BaseModel, Field, EmailStr
from src.models.enums import OrganizationType, OrganizationStatus, SubscriptionTier
from src.schemas.user import CreateUser
from datetime import datetime


class CreateOrganization(BaseModel):
    name: str = Field(..., description="The name of the organization")
    contact_email: EmailStr = Field(...,
                                    description="Contact email for the organization")
    organization_type: OrganizationType = Field(
        ..., description="The type of the organization")
    status: OrganizationStatus = Field(...,
                                       description="The status of the organization")
    subscription_tier: SubscriptionTier = Field(
        SubscriptionTier.FREE_TRIAL, description="The subscription tier of the organization")


class CreateOrganizationWithAdmin(BaseModel):
    organization: CreateOrganization
    admin_user: CreateUser


class CreateUserResponse(CreateUser):
    created_at: datetime
    updated_at: datetime


class CreateOrganizationResponse(CreateOrganization):
    organization: CreateOrganization
    admin_user: CreateUserResponse
    pass
