from dataclasses import dataclass

import httpx
import pydantic

from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.errors import C3GateWayError


class C3GatewayRequest(pydantic.BaseModel):
    filename: str


class C3GatewayResponse(pydantic.BaseModel):
    filename: str
    url: str


@dataclass(frozen=True, slots=True)
class HTTPC3Gateway(IC3GateWay):
    upload_image_url: str

    async def upload_image(self, image: bytes, filename: str) -> str:
        request = C3GatewayRequest(filename=filename)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.upload_image_url,
                files={"file": image},
                data=request.model_dump(mode="json"),
            )
            if not response.is_success:
                raise C3GateWayError
            return pydantic.TypeAdapter(C3GatewayResponse).validate_python(response.json()).url
