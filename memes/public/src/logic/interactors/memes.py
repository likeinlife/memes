import typing as tp
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass

from domain.entities.memes import Meme
from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.memes_interactor import IMemesInteractor
from infra.db.uow import UnitOfWork
from infra.repositories.memes.sqla import SQLAMemeRepository
from logic.usecases import memes

from .errors import InvalidImageExtensionError


@dataclass(frozen=True, eq=False, slots=True)
class MemesInteractor(IMemesInteractor):
    uow: UnitOfWork
    c3_gateway: IC3GateWay
    _allowed_extensions: tp.ClassVar[tuple[str, ...]] = ("jpg", "jpeg", "png")

    async def add(self, text: str, image: bytes, file_name: str) -> uuid.UUID:
        extension = self._check_image_extension(file_name)
        image_name = self._generate_image_name(extension)
        async with self._get_message_repo() as repository:
            return await memes.AddMemeUseCase(
                text=text,
                image=image,
                file_name=image_name,
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
        extension = self._check_image_extension(file_name)
        image_name = self._generate_image_name(extension)
        async with self._get_message_repo() as repository:
            return await memes.UpdateMemeUseCase(
                meme_id=meme_id,
                text=text,
                image=image,
                file_name=image_name,
                meme_repository=repository,
                c3_service=self.c3_gateway,
            )()

    def _check_image_extension(self, file_name: str) -> str:
        """Check file extension.

        Returns: extension
        """
        extension = file_name.lower().rsplit(".")[-1]
        if extension not in self._allowed_extensions:
            raise InvalidImageExtensionError(image_name=file_name)
        return extension

    def _generate_image_name(self, extension: str) -> str:
        return f"{uuid.uuid4()!s}.{extension}"

    @asynccontextmanager
    async def _get_message_repo(self) -> tp.AsyncIterator[SQLAMemeRepository]:
        async with self.uow as session:
            yield SQLAMemeRepository(session)
