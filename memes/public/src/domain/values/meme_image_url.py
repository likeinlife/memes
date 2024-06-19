from dataclasses import dataclass

import validators

from domain.values.base import BaseValueObject
from domain.values.errors import InvalidImageURLError


@dataclass
class MemeImageURL(BaseValueObject[str]):
    """Image url value object.

    Must be correct URL.
    """

    def validate(self) -> None:
        if not validators.url(self.value):
            raise InvalidImageURLError(self.value)
