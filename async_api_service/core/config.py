import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

DEFAULT_REDIS_PORT = 6379
DEFAULT_ES_PORT = 9200

REDIS_HOST = os.getenv('REDIS_HOST', 'redis_async_api')
REDIS_PORT = int(os.getenv('REDIS_PORT', DEFAULT_REDIS_PORT))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'etl_elasticsearch')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', DEFAULT_ES_PORT))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_ROUTE = (f"{os.getenv('AUTH_SERVICE_URL', 'http://auth_service')}:"
              f"{os.getenv('AUTH_SERVICE_PORT', '8000')}/api/v1/auth/authenticate_user_route")