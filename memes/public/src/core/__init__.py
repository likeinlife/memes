from functools import lru_cache

from .log import configure_logging
from .settings import Settings


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()


__all__ = ("get_settings", "configure_logging")
