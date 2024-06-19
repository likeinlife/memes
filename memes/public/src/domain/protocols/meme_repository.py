import typing as tp
import uuid

from annotated_types import Ge

from domain.entities.memes import Meme


class IMemeRepository(tp.Protocol):
    async def fetch_by_id(self, meme_id: uuid.UUID) -> Meme: ...

    async def fetch_list(self, limit: tp.Annotated[int, Ge(0)], offset: tp.Annotated[int, Ge(0)]) -> list[Meme]: ...

    async def add(self, meme: Meme) -> None: ...

    async def update(self, meme_id: uuid.UUID, image_url: str, text: str) -> Meme: ...

    async def delete(self, meme_id: uuid.UUID) -> None: ...
