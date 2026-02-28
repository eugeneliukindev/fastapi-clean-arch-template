from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=_NAMING_CONVENTION)

    def __repr__(self) -> str:
        cols = ", ".join(f"{c.name}={getattr(self, c.name)!r}" for c in self.__table__.columns)
        return f"<{self.__class__.__name__}({cols})>"
