from fastapi import APIRouter

from . import healthcheck


def register(router: APIRouter) -> None:
    _router = APIRouter(tags=["common"])
    _router.include_router(healthcheck.router)

    router.include_router(_router)
