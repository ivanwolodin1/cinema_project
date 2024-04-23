import os
from abc import ABC

from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class Config(ABC):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'auth_api')

    REDIS_HOST = os.getenv('REDIS_HOST', 'redis_async_api')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

    POSTGRES_USERNAME = os.getenv('POSTGRES_USER', 'app')
    POSTGRES_DB_NAME = os.getenv('POSTGRES_DB', 'user_auth_database')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres_auth')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    SQL_COMMAND_ECHO = False


class DevelopmentConfig(Config):
    SQL_COMMAND_ECHO = True


class ProductionConfig(Config):
    POSTGRES_HOST = 'db'


def get_config() -> Config:
    mode = os.getenv('PRODUCTION_MODE', '')
    if mode.lower() == 'true':
        return ProductionConfig()
    return DevelopmentConfig()


config = get_config()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('SECRET_KEY', 'secretkey')


@AuthJWT.load_config  # type: ignore
def get_config():  # type: ignore
    return Settings()
