import typing as tp
import uuid
from functools import partial

from dishka import Container
from fastapi import APIRouter, Depends, HTTPException, Path, Response, UploadFile, status

from container import get_container
from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.errors import C3GateWayError, MemeNotFoundError
from domain.protocols.memes_interactor import IMemesInteractor
from logic.interactors.errors import InvalidImageExtensionError

from . import mapper, schemas

router = APIRouter(tags=["memes"])


@router.get("/")
async def get_memes(
    paginator: tp.Annotated[schemas.Paginator, Depends()],
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeListResponse:
    with container() as req:
        interactor = req.get(IMemesInteractor)  # type: ignore
        memes = await interactor.fetch_list(limit=paginator.limit, offset=paginator.offset)
    image_getter = partial(router.url_path_for, "image")
    return mapper.MemesDomainSchemasMapper.to_response_list(memes, image_getter)


@router.get("/{id}/")
async def get_meme(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeResponse:
    with container() as req:
        interactor = req.get(IMemesInteractor)  # type: ignore
        try:
            memes = await interactor.fetch_by_id(meme_id=id)
        except MemeNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    image_getter = partial(router.url_path_for, "image")
    return mapper.MemesDomainSchemasMapper.to_response(memes, image_getter)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add(
    meme: tp.Annotated[schemas.MemeCreateRequest, Depends()],
    image: UploadFile,
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeCreateResponse:
    if not image.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image name is required")
    with container() as req:
        interactor = req.get(IMemesInteractor)  # type: ignore
        try:
            created = await interactor.add(text=meme.text, image=await image.read(), file_name=image.filename)
        except InvalidImageExtensionError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except C3GateWayError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    return schemas.MemeCreateResponse(meme_id=created)


@router.patch("/{id}/")
async def update(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    meme: tp.Annotated[schemas.MemeUpdateRequest, Depends()],
    image: UploadFile,
    container: tp.Annotated[Container, Depends(get_container)],
) -> schemas.MemeResponse:
    if not image.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image name is required")
    with container() as req:
        interactor = req.get(IMemesInteractor)  # type: ignore
        try:
            created = await interactor.update(
                meme_id=id,
                text=meme.text,
                image=await image.read(),
                file_name=image.filename,
            )
        except MemeNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except InvalidImageExtensionError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except C3GateWayError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)

    image_getter = partial(router.url_path_for, "image")
    return mapper.MemesDomainSchemasMapper.to_response(created, image_getter)


@router.delete("/{id}/")
async def delete(
    id: tp.Annotated[uuid.UUID, Path()],  # noqa: A002
    container: tp.Annotated[Container, Depends(get_container)],
) -> Response:
    with container() as req:
        interactor = req.get(IMemesInteractor)  # type: ignore
        try:
            await interactor.delete(meme_id=id)
        except MemeNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/image/{image_name}/")
async def image(
    image_name: tp.Annotated[str, Path()],
    container: tp.Annotated[Container, Depends(get_container)],
) -> Response:
    with container() as req:
        gateway_service = req.get(IC3GateWay)  # type: ignore
        try:
            content = await gateway_service.download_image(filename=image_name)
        except C3GateWayError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return Response(content=content, media_type="image/png")
