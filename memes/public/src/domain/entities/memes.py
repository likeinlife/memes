from dataclasses import dataclass

from domain.values.meme_image_url import MemeImageURL
from domain.values.meme_text import MemeText

from .base import BaseEntity


@dataclass(eq=False)
class Meme(BaseEntity):
    """Meme entity class."""

    image_url: MemeImageURL
    text: MemeText
    deleted: bool
