from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.core.enums import UserStatus
from src.schemas.base import PartialModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    status: UserStatus = UserStatus.ACTIVE


class UserPut(BaseModel):
    first_name: str
    last_name: str
    status: UserStatus = UserStatus.ACTIVE


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
