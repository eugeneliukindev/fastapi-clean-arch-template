from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import ConflictException, NotFoundException


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundException, _not_found_handler)
    app.add_exception_handler(ConflictException, _conflict_handler)


async def _not_found_handler(_: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


async def _conflict_handler(_: Request, exc: ConflictException) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})
