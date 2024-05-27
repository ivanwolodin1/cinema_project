import os

from motor import motor_asyncio


class Settings:
    PROJECT_NAME: str = 'Job Board'
    PROJECT_VERSION: str = '1.0.0'
    MAX_CONNECTIONS_COUNT = int(os.getenv('MAX_CONNECTIONS_COUNT', 10))
    MIN_CONNECTIONS_COUNT = int(os.getenv('MIN_CONNECTIONS_COUNT', 10))

    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
    MONGO_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'admin')
    MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'markqiu')

    MONGODB_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}'

    client: motor_asyncio.AsyncIOMotorClient = (
        motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    )

    database = client.likes

    SECRET_KEY = os.getenv('SECRET_KEY', 'our-secret-key')
    HASH_ALGORITHM = os.getenv('HASH_ALGORITHM', 'HS256')


settings = Settings()
AUTH_ROUTE = (
    f"{os.getenv('AUTH_SERVICE_URL', 'http://auth_service')}:"
    f"{os.getenv('AUTH_SERVICE_PORT', '8000')}/api/v1/auth/authenticate_user_route"
)
