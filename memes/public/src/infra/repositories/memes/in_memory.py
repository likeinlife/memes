import uuid
from dataclasses import dataclass, field

from domain.entities.memes import Meme
from domain.protocols.errors import MemeNotFoundError
from domain.protocols.meme_repository import IMemeRepository
from domain.values.meme_text import MemeText


@dataclass
class InMemoryMemeRepository(IMemeRepository):
    memes: dict[uuid.UUID, Meme] = field(default_factory=dict)

    async def fetch_by_id(self, meme_id: uuid.UUID) -> Meme:
        if not (meme := self.memes.get(meme_id)):
            raise MemeNotFoundError(meme_id=meme_id)
        if meme.deleted:
            raise MemeNotFoundError(meme_id=meme_id)
        return meme

    async def fetch_list(self, limit: int, offset: int) -> list[Meme]:
        return list(self.memes.values())[offset : offset + limit]

    async def add(self, meme: Meme) -> uuid.UUID:
        self.memes[meme.id] = meme
        return meme.id

    async def update(self, meme_id: uuid.UUID, image_name: str, text: str) -> Meme:
        meme = await self.fetch_by_id(meme_id)
        meme.image_name = image_name
        meme.text = MemeText(text)
        return self.memes[meme_id]

    async def delete(self, meme_id: uuid.UUID) -> None:
        meme = await self.fetch_by_id(meme_id)
        meme.deleted = True
