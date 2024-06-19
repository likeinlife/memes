import uuid
from dataclasses import dataclass

from src.domain.protocols.meme_repository import IMemeRepository
from src.logic.usecases.interface import IUseCase


@dataclass(frozen=True, eq=False, slots=True)
class DeleteMemeUseCase(IUseCase[None]):
    meme_id: uuid.UUID
    meme_repository: IMemeRepository

    async def __call__(self) -> None:
        return await self.meme_repository.delete(meme_id=self.meme_id)
