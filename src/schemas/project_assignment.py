from pydantic import BaseModel, Field


class AssignPollingUnitToProjectMember(BaseModel):
    """Assign Polling Unit to Projects Member
    - we could extend this to assign other entities in future
    """

    pu_coverage_ids: list[str] = Field(
        ..., description="The ID of the polling unit being assigned to the project member")
    user_id: str = Field(
        ..., description="The ID of the user being assigned the polling units")
    lga_coverage_id: str | None = Field(
        None, description="The ID of the LGA coverage for the project member")
    state_coverage_id: str | None = Field(
        None, description="The ID of the State coverage for the project member")
    ward_coverage_id: str = Field(
        ..., description="The IDs of the Ward coverages for the project member")
