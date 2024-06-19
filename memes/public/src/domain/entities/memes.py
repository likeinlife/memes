from dataclasses import dataclass

from domain.values.meme_text import MemeText

from .base import BaseEntity


@dataclass(eq=False)
class Meme(BaseEntity):
    """Meme entity class."""

    image_name: str
    text: MemeText
    deleted: bool
