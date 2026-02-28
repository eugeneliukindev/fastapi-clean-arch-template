from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import UserStatus

from .base import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(35))
    last_name: Mapped[str] = mapped_column(String(35))
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.ACTIVE)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
    )
