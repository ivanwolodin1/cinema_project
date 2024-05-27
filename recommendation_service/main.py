import uvicorn
import logging.config
from fastapi import FastAPI
from .config import get_settings
from .api import api_router
from .version import __version__
from .db import Base, engine


def create_db_tables():
    """Create all tables in database."""
    Base.metadata.create_all(engine)


def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fastapi application instance.
    """
    settings = get_settings()
    application = FastAPI(title=settings.PROJECT_NAME,
                          debug=settings.DEBUG,
                          version=__version__,
                          openapi_url=f"{settings.API_STR}/openapi.json")

    application.include_router(api_router, prefix=settings.API_STR)

    # application.add_event_handler("startup", startup_handler)
    # application.add_event_handler("shutdown", shutdown_handler)

    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # application.add_middleware(BaseHTTPMiddleware, dispatch=log_time)

    # create tables in db
    create_db_tables()

    return application


app = create_application()
settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
