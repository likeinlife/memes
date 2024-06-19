from dataclasses import dataclass

from domain.errors import BaseError


@dataclass(frozen=True, eq=False)
class EmptyTextError(BaseError):
    @property
    def message(self) -> str:
        return "Empty text"


@dataclass(frozen=True, eq=False)
class TextTooLongError(BaseError):
    max_length: int
    input_length: int

    @property
    def message(self) -> str:
        return f"Text too long. Max length: {self.max_length}. Input length: {self.input_length}"


@dataclass(frozen=True, eq=False)
class InvalidImageURLError(BaseError):
    file_url: str

    @property
    def message(self) -> str:
        return f"Invalid image URL: {self.file_url}"
