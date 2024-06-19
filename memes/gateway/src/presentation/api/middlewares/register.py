from fastapi import FastAPI

from . import log


def register(app: FastAPI) -> None:
    log.register(app)
