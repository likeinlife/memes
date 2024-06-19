import typing as tp
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

import httpx
import structlog

from domain.protocols.c3_gateway import IC3GateWay

from .errors import C3ImageDownloadError, C3ImageUploadError


@dataclass(frozen=True, slots=True)
class HTTPC3Gateway(IC3GateWay):
    url: str
    upload_uri: str = field(default="")
    download_uri: str = field(default="")
    _logger = structlog.get_logger()

    async def upload_image(self, image: bytes, filename: str) -> None:
        async with self.client() as client:
            response = await client.post(
                self.upload_uri,
                files={"file": (filename, image)},
            )
            if not response.is_success:
                self._logger.error(
                    "Error uploading image",
                    filename=filename,
                    status_code=response.status_code,
                    content=response.content,
                )
                raise C3ImageUploadError(filename)

    async def download_image(self, filename: str) -> bytes:
        async with self.client() as client:
            uri = f"{self.download_uri}/{filename}/"
            response = await client.get(uri)
            if not response.is_success:
                self._logger.error(
                    "Error downloading image",
                    filename=filename,
                    status_code=response.status_code,
                    content=response.content,
                )
                raise C3ImageDownloadError(filename)
            return response.content

    @asynccontextmanager
    async def client(self) -> tp.AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient(base_url=self.url) as client:
            yield client
