import typing as tp

from domain.entities.memes import Meme

from .schemas import MemeListResponse, MemeResponse


class RouteCreator(tp.Protocol):
    def __call__(self, *, image_name: str) -> str: ...


class MemesDomainSchemasMapper:
    @staticmethod
    def to_response(meme: Meme, route_creator: RouteCreator) -> MemeResponse:
        return MemeResponse(
            id=meme.id,
            image_url=route_creator(image_name=meme.image_name),
            text=meme.text.as_generic_type(),
            created_at=meme.created_at,
        )

    @staticmethod
    def to_response_list(memes: list[Meme], route_creator: RouteCreator) -> MemeListResponse:
        return MemeListResponse(items=[MemesDomainSchemasMapper.to_response(meme, route_creator) for meme in memes])
