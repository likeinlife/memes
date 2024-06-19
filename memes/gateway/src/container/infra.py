from dishka import Provider, Scope, provide
from minio import Minio

from core import get_settings
from domain.protocols.c3 import IC3Service
from infra.minio_client import get_minio_client
from infra.services.c3.minio_c3 import MinioC3


class InfraProvider(Provider):
    scope = Scope.APP

    @provide
    def _minio_client(self) -> Minio:
        settings = get_settings()
        return get_minio_client(
            settings.c3.url,
            settings.c3.access_key,
            settings.c3.secret_key,
            settings.c3.secure,
        )

    @provide
    def _c3_service(self, minio_client: Minio) -> IC3Service:
        settings = get_settings()
        return MinioC3(
            minio_client,
            settings.c3.bucket_name,
            settings.c3.encode_secret_key,
        )
