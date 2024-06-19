from dataclasses import dataclass

import httpx
import structlog

from domain.protocols.c3_gateway import IC3GateWay

from .errors import C3ImageUploadError


@dataclass(frozen=True, slots=True)
class HTTPC3Gateway(IC3GateWay):
    upload_image_url: str
    _logger = structlog.get_logger()

    async def upload_image(self, image: bytes, filename: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.upload_image_url,
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
