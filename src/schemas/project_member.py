from pydantic import BaseModel, Field
from src.models.enums import ProjectMemberStatus, ElectionRole
# from src.schemas.default import CamelCaseModel
# from src.schemas.locations import PollingUnitResponse, StateResponse


#

# schemas/location.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class StateResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LGAResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    state: Optional[StateResponse] = None

    model_config = ConfigDict(from_attributes=True)


class WardResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    lga: Optional[LGAResponse] = None

    model_config = ConfigDict(from_attributes=True)


class PollingUnitResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    ward: Optional[WardResponse] = None

    model_config = ConfigDict(from_attributes=True)


#

class AddProjectMember(BaseModel):
    """schema"""

    user_id: str = Field(..., description="user's id")
    role: ElectionRole = Field(
        default=ElectionRole.FIELD_AGENT, description="user's role in election project")
    status: ProjectMemberStatus = Field(
        default=ProjectMemberStatus.INVITED,
        description="current status of the member added to project")
    agent_code: str | None = None


class AddMultipleProjectMembers(BaseModel):
    """schema for adding multiple members to election project"""

    members: list[AddProjectMember]


class UserResponse(BaseModel):
    """schema for user response"""

    id: str
    full_name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class ProjectMemberResponse(BaseModel):
    """schema for project member response"""

    id: str
    user_id: str
    role: ElectionRole
    status: ProjectMemberStatus
    user: UserResponse

    model_config = {
        "from_attributes": True
    }


class AssignmentResponse(BaseModel):
    polling_unit: PollingUnitResponse

    model_config = {"from_attributes": True}


class ProjectAgentResponse(BaseModel):
    """schema for project agent response"""

    id: str
    user_id: str
    role: ElectionRole
    status: ProjectMemberStatus
    user: UserResponse

    model_config = {
        "from_attributes": True
    }


class AgentQueryParams(BaseModel):
    search: Optional[str] = None
    status: Optional[ProjectMemberStatus] = None
    state_id: Optional[str] = None
    lga_id: Optional[str] = None
    ward_id: Optional[str] = None
