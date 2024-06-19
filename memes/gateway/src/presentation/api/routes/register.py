from fastapi import APIRouter, FastAPI

from . import c3, common


def register(app: FastAPI) -> None:
    """Register all routes."""
    router = APIRouter()
    common.register(router)
    c3.register(router)

    app.include_router(router)
