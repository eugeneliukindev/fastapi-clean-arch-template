from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.core.uow import UoWDep
from src.domain.exceptions import NotFoundException
from src.models.users import User
from src.schemas.users import UserCreate, UserPatch, UserPut


class UsersService:
    def __init__(self, uow: UoWDep):
        self.uow = uow

    async def get(self, id_: UUID) -> User:
        user = await self.uow.users.get(id_)
        if not user:
            raise NotFoundException(f"User {id_} not found")
        return user

    async def count(self) -> int:
        return await self.uow.users.count()

    async def get_all(self, offset: int = 0, limit: int = 20) -> list[User]:
        return await self.uow.users.get_all(offset=offset, limit=limit)

    async def create(self, data: UserCreate) -> User:
        user = await self.uow.users.create(data)
        await self.uow.commit()
        return user

    async def update(self, id_: UUID, data: UserPut | UserPatch) -> User:
        user = await self.uow.users.update(id_, data)
        if not user:
            raise NotFoundException(f"User {id_} not found")
        await self.uow.commit()
        return user

    async def delete(self, id_: UUID) -> User:
        user = await self.uow.users.delete(id_)
        if not user:
            raise NotFoundException(f"User {id_} not found")
        await self.uow.commit()
        return user


UserServiceDep = Annotated[UsersService, Depends()]
