from uuid import UUID

from pydantic import BaseModel as PydanticModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseEntity


class BaseRepository[T: BaseEntity, C: PydanticModel, U: PydanticModel]:
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id_: UUID) -> T | None:
        return await self.session.get(self.model, id_)

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, data: C) -> T:
        result = await self.session.execute(insert(self.model).values(**data.model_dump()).returning(self.model))
        return result.scalar_one()

    async def update(self, id_: UUID, data: U) -> T | None:
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id_)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        return result.scalar_one_or_none()

    async def delete(self, id_: UUID) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == id_))
