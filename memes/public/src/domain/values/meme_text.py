from dataclasses import dataclass

from domain import constants
from domain.values import errors
from domain.values.base import BaseValueObject


@dataclass
class MemeText(BaseValueObject[str]):
    """Text value object.

    Text must be not empty and less than MAX_MESSAGE_LEN symbols
    """

    def validate(self) -> None:
        if not self.value:
            raise errors.EmptyTextError
        if len(self.value) > constants.MAX_TEXT_LEN:
            raise errors.TextTooLongError(
                max_length=constants.MAX_TEXT_LEN,
                input_length=len(self.value),
            )
