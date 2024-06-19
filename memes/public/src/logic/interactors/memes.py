import typing as tp
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass

from src.domain.entities.memes import Meme
from src.domain.protocols.c3_gateway import IC3GateWay
from src.infra.db.uow import UnitOfWork
from src.infra.repositories.memes.sqla import SQLAMemeRepository
from src.logic.usecases import memes


@dataclass(frozen=True, eq=False, slots=True)
class MemesInteractor:
    uow: UnitOfWork
    c3_gateway: IC3GateWay

    async def add(self, text: str, image: bytes, file_name: str) -> uuid.UUID:
        async with self._get_message_repo() as repository:
            return await memes.AddMemeUseCase(
                text=text,
                image=image,
                file_name=file_name,
                meme_repository=repository,
                c3_service=self.c3_gateway,
            )()

    async def fetch_by_id(self, meme_id: uuid.UUID) -> Meme:
        async with self._get_message_repo() as repository:
            return await memes.FetchMemeUseCase(
                meme_id=meme_id,
                meme_repository=repository,
            )()

    async def fetch_list(self, limit: int, offset: int) -> list[Meme]:
        async with self._get_message_repo() as repository:
            return await memes.FetchMemeListUseCase(
                limit=limit,
                offset=offset,
                meme_repository=repository,
            )()

    async def delete(self, meme_id: uuid.UUID) -> None:
        async with self._get_message_repo() as repository:
            return await memes.DeleteMemeUseCase(
                meme_id=meme_id,
                meme_repository=repository,
            )()

    async def update(self, meme_id: uuid.UUID, text: str, image: bytes, file_name: str) -> Meme:
        async with self._get_message_repo() as repository:
            return await memes.UpdateMemeUseCase(
                meme_id=meme_id,
                text=text,
                image=image,
                file_name=file_name,
                meme_repository=repository,
                c3_service=self.c3_gateway,
            )()

    @asynccontextmanager
    async def _get_message_repo(self) -> tp.AsyncIterator[SQLAMemeRepository]:
        async with self.uow as session:
            yield SQLAMemeRepository(session)
