from minio import Minio


def get_minio_client(url: str, access_key: str, secret_key: str, secure: bool = False) -> Minio:
    return Minio(
        url,
        access_key,
        secret_key,
        secure=secure,
    )
