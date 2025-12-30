from pydantic import BaseModel, Field


class AssignPollingUnitToProjectMember(BaseModel):
    """Assign Polling Unit to Projects Member
    - we could extend this to assign other entities in future
    """

    polling_unit_ids: list[str] = Field(
        ..., description="The ID of the polling unit being assigned to the project member")
    user_id: str = Field(
        ..., description="The ID of the user being assigned the polling units")
