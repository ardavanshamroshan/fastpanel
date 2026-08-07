import logging

from fastapi import FastAPI

from app.helpers.logging import setup_logging
from config.settings import get_settings
from routes.api import api_router
from routes.web import router as web_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
    )

    app.include_router(web_router)
    app.include_router(api_router)

    logger.info("App started env=%s", settings.app_env)

    return app


app = create_app()
