from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Annotated, Any

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncEngine


class DatabaseManager:
    def __init__(self, url: str | URL, **engine_kw: Any):
        self.engine: AsyncEngine = create_async_engine(url=url, **engine_kw)
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        self.session_factory = asynccontextmanager(self.session_getter)

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_maker() as session:
            yield session


db_manager = DatabaseManager(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

SessionDep = Annotated[AsyncSession, Depends(db_manager.session_getter)]
