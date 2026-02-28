from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, server_default=func.uuidv7())
