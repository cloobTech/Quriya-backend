from datetime import datetime
from pydantic import BaseModel, field_validator, Field
from src.models.enums import ElectionStatus, ResultStatus
from src.schemas.locations import PUResponse
from src.schemas.result import ResultResponseSchema
from src.schemas.incidents import IncidentSchema


class CoverageSelection(BaseModel):
    state_ids: list[str] = []
    lga_ids: list[str] = []
    ward_ids: list[str] = []
    polling_unit_ids: list[str] = []

    @field_validator('*')
    @classmethod
    def remove_duplicates(cls, v):
        """remove duplicates"""
        if isinstance(v, list):
            return list(set(v))
        return v


class StateCoverageOut(BaseModel):
    id: str
    name: str
    status: ElectionStatus

    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            id=obj.id,
            name=obj.state.name,
            status=obj.status
        )

    model_config = {
        "from_attributes": True
    }


class LGAOut(BaseModel):
    id: str
    name: str
    status: ElectionStatus

    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            id=obj.id,
            name=obj.lga.name,
            status=obj.status
        )

    model_config = {
        "from_attributes": True
    }


class WardOut(BaseModel):
    id: str
    name: str
    status: ElectionStatus

    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            id=obj.id,
            name=obj.ward.name,
            status=obj.status
        )

    model_config = {
        "from_attributes": True
    }


class PollingUnitOut(BaseModel):
    id: str
    name: str
    status: ElectionStatus

    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            id=obj.id,
            name=obj.polling_unit.name,
            status=obj.status
        )

    model_config = {
        "from_attributes": True
    }


class PUQueryParams(BaseModel):
    search: str | None = None
    status: ElectionStatus | None = None
    ward_id: str | None = None
    lga_id: str | None = None
    state_id: str | None = None
    result_status: ResultStatus | None = None
    incident_reported: bool | None = None
    assigned: bool | None = None
    unassigned: bool | None = None


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class DetailedPollingUnitOutput(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    status: ElectionStatus
    polling_unit: PUResponse
    # ward: WardOut
    user: UserResponse | None = None
    result: ResultResponseSchema | None = None
    incidents: list[IncidentSchema] = []

    @classmethod
    def model_validate(cls, obj, **kwargs):
        return cls(
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            id=obj.id,
            user=obj.assignment.member.user if (
                obj.assignment and obj.assignment.member)else None,
            status=obj.status,
            polling_unit=obj.polling_unit,
            result=obj.polling_units_result,
            incidents=obj.incidents

        )

    model_config = {
        "from_attributes": True
    }
