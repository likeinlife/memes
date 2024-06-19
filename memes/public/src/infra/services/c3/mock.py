from domain.protocols.c3_gateway import IC3GateWay


class MockC3Gateway(IC3GateWay):
    async def upload_image(self, image: bytes, filename: str) -> str:  # noqa: ARG002
        return f"https://example.com/{filename}"
