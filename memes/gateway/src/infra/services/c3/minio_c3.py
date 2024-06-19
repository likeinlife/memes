import io
from dataclasses import dataclass

import structlog
from minio import Minio

from domain.protocols.c3 import IC3Service


@dataclass(frozen=True, eq=False, slots=True)
class MinioC3(IC3Service):
    client: Minio
    bucket_name: str
    encode_secret_key: bytes
    _logger = structlog.get_logger()

    def __post_init__(self) -> None:
        if not self._bucket_exists():
            self._make_bucket()

    async def upload_image(self, image: bytes, filename: str) -> None:
        self.client.put_object(
            self.bucket_name,
            filename,
            io.BytesIO(image),
            len(image),
        )

    async def download_image(self, filename: str) -> bytes:
        response = self.client.get_object(
            self.bucket_name,
            filename,
        )
        return response.read()

    def _make_bucket(self) -> None:
        self.client.make_bucket(self.bucket_name)

    def _bucket_exists(self) -> bool:
        self._logger.debug("Create bucket", bucket_name=self.bucket_name)
        return self.client.bucket_exists(self.bucket_name)
