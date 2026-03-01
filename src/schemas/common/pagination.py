from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class PaginationParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100, alias="per_page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


Pagination = Annotated[PaginationParams, Query()]
