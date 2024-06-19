import pytest

from domain.constants import MAX_TEXT_LEN
from domain.values.errors import TextTooLongError
from domain.values.meme_text import MemeText


def test_meme_text_value_object_raises_error_on_invalid_text():
    value = "t" * (MAX_TEXT_LEN + 1)
    with pytest.raises(TextTooLongError):
        MemeText(value)


def test_meme_text_value_object_validates_text():
    value = "t" * (MAX_TEXT_LEN - 1)
    assert MemeText(value).as_generic_type() == value
