import uvicorn
from api.v1.account import protected_router as account_router
from api.v1.auth import router as auth_router
from core.config import config
from core.middleware import handle_exceptions
from db_connectors import redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.middleware('http')(handle_exceptions)


async def startup_event():
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


async def shutdown_event():
    await redis.redis.close()


app.add_event_handler('startup', startup_event)
app.add_event_handler('shutdown', shutdown_event)

app.include_router(auth_router, prefix='/api/v1/auth', tags=['Auth'])
app.include_router(
    account_router,
    prefix='/api/v1/auth',
    tags=['Protected'],
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
