from types import TracebackType

from sqlalchemy.ext import asyncio as sa_async


class UnitOfWork:
    def __init__(self, session_maker: sa_async.async_sessionmaker[sa_async.AsyncSession]) -> None:
        self.session_maker = session_maker

    async def __aenter__(self) -> sa_async.AsyncSession:
        self._session = self.session_maker()
        return self._session

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
