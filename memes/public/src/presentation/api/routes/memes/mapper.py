from domain.entities.memes import Meme

from .schemas import MemeListResponse, MemeResponse


class MemesDomainSchemasMapper:
    @staticmethod
    def to_response(meme: Meme) -> MemeResponse:
        return MemeResponse(
            id=meme.id,
            image_url=meme.image_url.as_generic_type(),
            text=meme.text.as_generic_type(),
            created_at=meme.created_at,
        )

    @staticmethod
    def to_response_list(memes: list[Meme]) -> MemeListResponse:
        return MemeListResponse(items=[MemesDomainSchemasMapper.to_response(meme) for meme in memes])
