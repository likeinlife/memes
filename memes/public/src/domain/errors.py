from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BaseError(Exception):
    """Base error."""

    @property
    def message(self) -> str:
        return "Base error message"

    def __str__(self) -> str:
        """Return error message."""
        return self.message
