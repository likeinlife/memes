import logging
import typing as tp
from logging.config import dictConfig

import structlog
from structlog.types import EventDict


def configure_logging(level: str, json_format: bool) -> None:
    _configure_structlog()
    dictConfig(_get_logging_settings(level, json_format))


def _healthcheck_filter_processor(_, __, event_dict: EventDict) -> EventDict:  # noqa: ANN001
    if "health" in event_dict.get("path", ""):
        raise structlog.DropEvent
    return event_dict


def _configure_structlog() -> None:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            _healthcheck_filter_processor,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=structlog.threadlocal.wrap_dict(dict),
        cache_logger_on_first_use=True,
    )


def _get_logging_settings(level: str, json_format: bool) -> dict[str, tp.Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "keep_exc_info": True,
            },
            "plain_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "keep_exc_info": True,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": ("json_console" if json_format else "plain_console"),
                "level": level,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": level,
            },
            "jaeger": {"level": logging.ERROR},
            "uvicorn.access": {"level": logging.ERROR},
            "uvicorn.error": {"level": logging.ERROR},
        },
    }
