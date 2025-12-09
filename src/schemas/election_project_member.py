from pydantic import BaseModel, Field
from datetime import datetime
from src.models.enums import ElectionProjectMemberStatus, ElectionRole


class AddElectionProjectMember(BaseModel):
    """schema"""

    user_id: str
    election_project_id: str
    role: ElectionRole
    status: ElectionProjectMemberStatus = Field(
        default=ElectionProjectMemberStatus.INVITED,
        description="current status of the member added to project")
