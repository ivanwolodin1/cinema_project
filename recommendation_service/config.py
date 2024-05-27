import os
import logging
from functools import lru_cache
from typing import Optional, Any

from pydantic import BaseModel, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings
from .utils.logging import StandardFormatter, ColorFormatter


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: dict
    handlers: dict
    loggers: dict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'recsys_api'
    PROJECT_SLUG: str = 'recsys_api'

    DEBUG: bool = True
    API_STR: str = "/api/v1"

    # ########################### DB Configuration ############################
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
    # set the default value to None, such that the assemble_db_connection can
    # build the URI for us and do checks.
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # noinspection PyMethodParameters
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(
            cls, v: Optional[str], values: ValidationInfo) -> str:
        """Assemble the postgres DB URI with the provided POSTGRES_SERVER,
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

        Args:
            v (Optional[str]): the value of defined SQLALCHEMY_DATABASE_URI.
            values (Dict[str, Any]): a dictionary contains the requisite values.

        Returns:
            str: the postgres DB URI.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=values.data.get("POSTGRES_PORT"),
            path=values.data.get('POSTGRES_DB') or '',
        ).unicode_string()

    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'colorFormatter': {'()': ColorFormatter},
            'standardFormatter': {'()': StandardFormatter},
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "DEBUG",
                'formatter': 'standardFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "recsys_api": {
                'handlers': ['consoleHandler'],
                'level': "DEBUG",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                # Use the project logger to replace uvicorn.access logger
                'handlers': []
            }
        }
    }

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    """Get settings object, and use cache to speed up the execution.

    Returns:
        object: The instance of the current used settings class.
    """
    base_settings = Settings()
    logger = logging.getLogger(base_settings.PROJECT_SLUG)
    return base_settings
