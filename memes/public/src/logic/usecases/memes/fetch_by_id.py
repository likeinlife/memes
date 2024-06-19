import uuid
from dataclasses import dataclass

from domain.entities.memes import Meme
from domain.protocols.meme_repository import IMemeRepository
from logic.usecases.interface import IUseCase


@dataclass(frozen=True, eq=False, slots=True)
class FetchMemeUseCase(IUseCase[Meme]):
    meme_id: uuid.UUID
    meme_repository: IMemeRepository

    async def __call__(self) -> Meme:
        return await self.meme_repository.fetch_by_id(meme_id=self.meme_id)
