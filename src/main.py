from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.api.exception_handlers import register_exception_handlers
from src.core.database import db_manager


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await db_manager.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
