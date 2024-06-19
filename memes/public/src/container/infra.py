from dishka import Provider, Scope, provide
from sqlalchemy.ext import asyncio as sa_async

from core.settings import settings
from domain.protocols.c3_gateway import IC3GateWay
from infra.db.base import create_async_engine, create_session_maker
from infra.db.uow import UnitOfWork
from infra.services.c3.http_service import HTTPC3Gateway


class InfraProvider(Provider):
    scope = Scope.APP

    @provide
    def _engine(self) -> sa_async.AsyncEngine:
        return create_async_engine(settings.db.get_url())

    @provide
    def _sessionmaker(self, engine: sa_async.AsyncEngine) -> sa_async.async_sessionmaker:
        return create_session_maker(engine)

    @provide
    def _uow(self, session_maker: sa_async.async_sessionmaker) -> UnitOfWork:
        return UnitOfWork(session_maker)

    @provide
    def _c3(self) -> IC3GateWay:
        return HTTPC3Gateway(settings.c3.url)
