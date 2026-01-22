from pydantic import BaseModel, Field
from typing import Any


class DefaultResponse(BaseModel):
    message: str
    data: Any  # Replace `Any` with a more specific schema if possible


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class Meta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel):
    data: list[Any]  
    meta: Meta
