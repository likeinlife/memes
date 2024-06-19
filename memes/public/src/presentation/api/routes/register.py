from fastapi import APIRouter, FastAPI

from . import common, memes


def register(app: FastAPI) -> None:
    """Register all routes."""
    router = APIRouter()
    common.register(router)
    memes.register(router)

    app.include_router(router)
