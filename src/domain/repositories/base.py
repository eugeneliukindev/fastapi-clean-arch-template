from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseEntity


class BaseRepository[T: BaseEntity, C: BaseModel, U: BaseModel]:
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id_: UUID) -> T | None:
        return await self.session.get(self.model, id_)

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def get_all(self, offset: int = 0, limit: int | None = None) -> list[T]:
        query = select(self.model).offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, data: C) -> T:
        result = await self.session.execute(insert(self.model).values(**data.model_dump()).returning(self.model))
        return result.scalar_one()

    async def update(self, id_: UUID, data: U) -> T | None:
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id_)
            .values(data.model_dump(exclude_unset=True))  # for patch http methods
            .returning(self.model)
        )
        return result.scalar_one_or_none()

    async def delete(self, id_: UUID) -> T | None:
        result = await self.session.execute(delete(self.model).where(self.model.id == id_).returning(self.model))
        return result.scalar_one_or_none()
