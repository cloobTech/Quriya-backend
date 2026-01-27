from pydantic import BaseModel, field_validator
from src.models.enums import ElectionStatus, ResultStatus


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
