import typing as tp


class IC3GateWay(tp.Protocol):
    async def upload_image(self, image: bytes, filename: str) -> str:
        """Upload image to cloud storage.

        Returns: image url
        """
        ...
