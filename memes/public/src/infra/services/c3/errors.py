from dataclasses import dataclass

from domain.protocols.errors import C3GateWayError


@dataclass(eq=False)
class C3ImageUploadError(C3GateWayError):
    filename: str

    @property
    def message(self) -> str:
        return f"Error uploading image {self.filename}"
