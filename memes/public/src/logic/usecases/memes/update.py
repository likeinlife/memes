import uuid
from dataclasses import dataclass

from domain.entities.memes import Meme
from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.meme_repository import IMemeRepository
from logic.usecases.interface import IUseCase


@dataclass(frozen=True, eq=False, slots=True)
class UpdateMemeUseCase(IUseCase[Meme]):
    meme_id: uuid.UUID
    text: str
    image: bytes
    file_name: str
    meme_repository: IMemeRepository
    c3_service: IC3GateWay

    async def __call__(self) -> Meme:
        image_url = await self.c3_service.upload_image(self.image, self.file_name)
        return await self.meme_repository.update(meme_id=self.meme_id, image_url=image_url, text=self.text)
