from domain.protocols.c3_gateway import IC3GateWay


class MockC3Gateway(IC3GateWay):
    async def upload_image(self, image: bytes, filename: str) -> None:  # noqa: ARG002
        return None

    async def download_image(self, filename: str) -> bytes:  # noqa: ARG002
        return b"Opachki"
