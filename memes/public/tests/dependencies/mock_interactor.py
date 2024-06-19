import typing as tp
import uuid
from dataclasses import dataclass
from functools import lru_cache

from domain.entities.memes import Meme
from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.memes_interactor import IMemesInteractor
from infra.repositories.memes.in_memory import InMemoryMemeRepository
from logic.interactors.errors import InvalidImageExtensionError
from logic.usecases import memes


@dataclass(frozen=True, eq=False)
class MockMemesInteractor(IMemesInteractor):
    c3_gateway: IC3GateWay
    _allowed_extensions: tp.ClassVar[tuple[str, ...]] = ("jpg", "jpeg", "png")

    async def add(self, text: str, image: bytes, file_name: str) -> uuid.UUID:
        extension = self._check_image_extension(file_name)
        image_name = self._generate_image_name(extension)
        repository = self._get_message_repo()
        return await memes.AddMemeUseCase(
            text=text,
            image=image,
            file_name=image_name,
            meme_repository=repository,
            c3_service=self.c3_gateway,
        )()

    async def fetch_by_id(self, meme_id: uuid.UUID) -> Meme:
        repository = self._get_message_repo()
        return await memes.FetchMemeUseCase(
            meme_id=meme_id,
            meme_repository=repository,
        )()

    async def fetch_list(self, limit: int, offset: int) -> list[Meme]:
        repository = self._get_message_repo()
        return await memes.FetchMemeListUseCase(
            limit=limit,
            offset=offset,
            meme_repository=repository,
        )()

    async def delete(self, meme_id: uuid.UUID) -> None:
        repository = self._get_message_repo()
        return await memes.DeleteMemeUseCase(
            meme_id=meme_id,
            meme_repository=repository,
        )()

    async def update(self, meme_id: uuid.UUID, text: str, image: bytes, file_name: str) -> Meme:
        extension = self._check_image_extension(file_name)
        image_name = self._generate_image_name(extension)
        repository = self._get_message_repo()
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

    @lru_cache(1)  # noqa: B019
    def _get_message_repo(self) -> InMemoryMemeRepository:
        return InMemoryMemeRepository()
