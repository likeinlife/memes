import typing as tp
import uuid

from dishka import Container
from fastapi import APIRouter, Depends, File, HTTPException, Path, Response, status

from container import get_container
from domain.protocols.errors import MemeNotFoundError
from logic.interactors.memes import MemesInteractor

from . import mapper, schemas

router = APIRouter(tags=["memes"])


@router.get("/")
async def get_memes(
    paginator: tp.Annotated[schemas.Paginator, Depends()],
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeListResponse:
    interactor = container.get(MemesInteractor)
    memes = await interactor.fetch_list(limit=paginator.limit, offset=paginator.offset)
    return mapper.MemesDomainSchemasMapper.to_response_list(memes)


@router.get("/{id}/")
async def get_meme(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeResponse:
    interactor = container.get(MemesInteractor)
    try:
        memes = await interactor.fetch_by_id(meme_id=id)
    except MemeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return mapper.MemesDomainSchemasMapper.to_response(memes)


@router.post("/")
async def add(
    meme: tp.Annotated[schemas.MemeCreateRequest, Depends()],
    image: tp.Annotated[bytes, File()],
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeCreateResponse:
    interactor = container.get(MemesInteractor)
    created = await interactor.add(text=meme.text, image=image, file_name=meme.image_name)
    return schemas.MemeCreateResponse(meme_id=created)


@router.patch("/{id}/")
async def update(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    meme: tp.Annotated[schemas.MemeUpdateRequest, Depends()],
    image: tp.Annotated[bytes, File()],
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeUpdateResponse:
    interactor = container.get(MemesInteractor)
    try:
        created = await interactor.update(meme_id=id, text=meme.text, image=image, file_name=meme.image_name)
    except MemeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return schemas.MemeUpdateResponse(
        id=created.id,
        image_url=created.image_url.as_generic_type(),
        text=created.text.as_generic_type(),
        created_at=created.created_at,
    )


@router.delete("/{id}/")
async def delete(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    container: tp.Annotated[Container, Depends(get_container)],
) -> Response:
    interactor = container.get(MemesInteractor)
    try:
        await interactor.delete(meme_id=id)
    except MemeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return Response(status.HTTP_204_NO_CONTENT)
