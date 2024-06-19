import abc
import typing as tp
from dataclasses import dataclass

V = tp.TypeVar("V")


@dataclass
class BaseValueObject(abc.ABC, tp.Generic[V]):
    """Base value object."""

    value: V

    def __post_init__(self) -> None:
        """Validate value on init."""
        self.validate()

    @abc.abstractmethod
    def validate(self) -> None:
        """Validate value."""

    def as_generic_type(self) -> V:
        """Get value from ValueObject."""
        return self.value
