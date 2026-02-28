from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.core.enums import UserStatus
from src.schemas.base import PartialModel


class UserCreate(BaseModel):
    first_name: Annotated[str, StringConstraints(min_length=4, max_length=35)]
    last_name: Annotated[str, StringConstraints(min_length=4, max_length=35)]
    status: UserStatus = UserStatus.ACTIVE


class UserPut(UserCreate):
    pass


class UserPatch(UserPut, PartialModel):
    pass


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime
