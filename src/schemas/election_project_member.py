from pydantic import BaseModel, Field
from src.models.enums import ProjectMemberStatus, ElectionRole


class AddProjectMember(BaseModel):
    """schema"""

    user_id: str = Field(..., description="user's id")
    role: ElectionRole
    status: ProjectMemberStatus = Field(
        default=ProjectMemberStatus.INVITED,
        description="current status of the member added to project")


class AddMultipleProjectMembers(BaseModel):
    """schema for adding multiple members to election project"""

    members: list[AddProjectMember]
