import uuid
from dataclasses import dataclass

from domain.errors import BaseError


@dataclass(eq=False)
class MemeNotFoundError(BaseError):
    meme_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Meme with id {self.meme_id} not found"


class C3GateWayError(BaseError):
    @property
    def message(self) -> str:
        return "C3 gateway error"
