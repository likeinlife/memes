import typing as tp


class IC3Service(tp.Protocol):
    async def upload_image(self, image: bytes, filename: str) -> None:
        """Upload image to cloud storage."""
        ...

    async def download_image(self, filename: str) -> bytes: ...
