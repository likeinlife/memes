from dataclasses import dataclass

from domain.errors import BaseError


@dataclass
class InvalidImageExtensionError(BaseError):
    image_name: str

    @property
    def message(self) -> str:
        return f"Invalid image extension {self.image_name}"
