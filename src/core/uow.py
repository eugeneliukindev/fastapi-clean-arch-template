from collections.abc import AsyncGenerator
from typing import Annotated, Self

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.user import UserRepository

from .database import SessionDep


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @classmethod
    async def getter(cls, session: SessionDep) -> AsyncGenerator[Self, None]:
        self = cls(session)
        try:
            yield self
        except BaseException:
            await self.rollback()
            raise


UoWDep = Annotated[UnitOfWork, Depends(UnitOfWork.getter)]
