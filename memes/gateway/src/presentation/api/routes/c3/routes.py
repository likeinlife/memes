import typing as tp
import uuid

from fastapi import APIRouter, Path, Response, UploadFile

from container import get_container
from domain.protocols.c3 import IC3Service

router = APIRouter()


@router.post("/")
async def upload(
    file: UploadFile,
) -> None:
    container = get_container()
    c3_service = container.get(IC3Service)  # type: ignore
    filename = file.filename or str(uuid.uuid4())
    await c3_service.upload_image(image=file.file.read(), filename=filename)


@router.get("/{file_name}/")
async def download(
    file_name: tp.Annotated[str, Path()],
) -> Response:
    container = get_container()
    c3_service = container.get(IC3Service)  # type: ignore
    file = await c3_service.download_image(filename=file_name)
    return Response(content=file, media_type="image/png")
