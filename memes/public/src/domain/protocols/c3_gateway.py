import typing as tp


class IC3GateWay(tp.Protocol):
    async def upload_image(self, image: bytes, filename: str) -> None:
        """Upload image to cloud storage."""
        ...
