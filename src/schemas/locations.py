from pydantic import BaseModel, Field


class StateResponse(BaseModel):
    id: str
    name: str

    model_config = {
        "from_attributes": True
    }


class LgaResponse(BaseModel):
    id: str
    name: str
    state_id: str

    model_config = {
        "from_attributes": True
    }


class WardResponse(BaseModel):
    id: str
    name: str
    lga_id: str

    model_config = {
        "from_attributes": True
    }


class PollingUnitResponse(BaseModel):
    id: str
    name: str
    code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_source: str | None = None
    ward_id: str
    formatted_address: str | None = None

    model_config = {
        "from_attributes": True
    }


class PUResponse(PollingUnitResponse):
    id: str = Field(exclude=True)
    ward_id: str = Field(exclude=True)

    model_config = {
        "from_attributes": True
    }
