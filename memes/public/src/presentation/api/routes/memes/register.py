from fastapi import APIRouter

from . import routes


def register(router: APIRouter) -> None:
    _router = APIRouter(prefix="/memes", tags=["memes"])
    _router.include_router(routes.router)

    router.include_router(_router)
