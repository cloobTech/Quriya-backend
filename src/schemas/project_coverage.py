from pydantic import BaseModel, field_validator


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