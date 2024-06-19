import datetime as dt
import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sa_async


def create_async_engine(url: str, echo: bool = False) -> sa_async.AsyncEngine:
    return sa_async.create_async_engine(url, echo=echo)


def create_sync_engine(url: str, echo: bool = False) -> sa.Engine:
    return sa.create_engine(url, echo=echo)


def create_session_maker(engine: sa_async.AsyncEngine) -> sa_async.async_sessionmaker:
    return sa_async.async_sessionmaker(bind=engine)


class Base(orm.MappedAsDataclass, orm.DeclarativeBase):
    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        init=False,
        default_factory=uuid.uuid4,
    )
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(server_default=sa.func.now(), init=False)


def create_tables(url: str) -> None:
    engine = create_sync_engine(url)
    Base.metadata.create_all(engine)
