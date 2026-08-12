import logging

from config.settings import get_settings


def setup_logging():
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.logging.log_level.upper(), logging.INFO),
        format=settings.logging.log_format,
    )
