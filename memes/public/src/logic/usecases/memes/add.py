import uuid
from dataclasses import dataclass

from domain.entities.memes import Meme
from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.meme_repository import IMemeRepository
from domain.values.meme_image_url import MemeImageURL
from domain.values.meme_text import MemeText
from logic.usecases.interface import IUseCase


@dataclass(frozen=True, eq=False, slots=True)
class AddMemeUseCase(IUseCase[uuid.UUID]):
    text: str
    image: bytes
    file_name: str
    meme_repository: IMemeRepository
    c3_service: IC3GateWay

    async def __call__(self) -> uuid.UUID:
        image_url = await self.c3_service.upload_image(self.image, self.file_name)
        meme = Meme(
            text=MemeText(self.text),
            image_url=MemeImageURL(image_url),
            deleted=False,
        )
        return await self.meme_repository.add(meme=meme)
