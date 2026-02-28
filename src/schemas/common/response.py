import math
from typing import Any

from pydantic import BaseModel, computed_field, model_serializer
from pydantic.functional_serializers import SerializerFunctionWrapHandler


class _ExcludeNoneModel(BaseModel):
    @model_serializer(mode="wrap")
    def _exclude_none(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        return {k: v for k, v in handler(self).items() if v is not None}


class Meta(_ExcludeNoneModel):
    total: int | None = None
    page: int | None = None
    per_page: int | None = None

    @computed_field
    @property
    def total_pages(self) -> int | None:
        if self.total is None or self.per_page is None:
            return None
        return math.ceil(self.total / self.per_page)


class ApiResponse[T](_ExcludeNoneModel):
    data: T
    message: str | None = None
    meta: Meta | None = None
