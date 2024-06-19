import typing as tp
from dataclasses import dataclass

from annotated_types import Ge

from src.domain.entities.memes import Meme
from src.domain.protocols.meme_repository import IMemeRepository
from src.logic.usecases.interface import IUseCase


@dataclass(frozen=True, eq=False, slots=True)
class FetchMemeListUseCase(IUseCase[list[Meme]]):
    meme_repository: IMemeRepository
    limit: tp.Annotated[int, Ge(0)]
    offset: tp.Annotated[int, Ge(0)]

    async def __call__(self) -> list[Meme]:
        return await self.meme_repository.fetch_list(limit=self.limit, offset=self.offset)
