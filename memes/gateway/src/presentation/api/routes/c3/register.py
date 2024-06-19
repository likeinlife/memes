from fastapi import APIRouter

from . import routes


def register(router: APIRouter) -> None:
    _router = APIRouter(prefix="/c3", tags=["c3"])
    _router.include_router(routes.router)

    router.include_router(_router)
