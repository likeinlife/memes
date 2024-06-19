from fastapi import FastAPI

from . import base_error, validation_error


def register(app: FastAPI) -> None:
    base_error.register(app)
    validation_error.register(app)
