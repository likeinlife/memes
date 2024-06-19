from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import configure_logging, get_settings

from . import error_handlers, middlewares, routes

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, ANN201
    configure_logging(settings.log.level, settings.log.json_format)
    yield


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

error_handlers.register(app)
middlewares.register(app)
routes.register(app)
