import os

import uvicorn
from api.v1.auth_service import auther
from api.v1.favorite import favoriter
from api.v1.like import liker
from api.v1.review import reviewer
from db.mongo_utils import close_mongo_connection, connect_to_mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title='UGC',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    )


app.add_event_handler('startup', connect_to_mongo)
app.add_event_handler('shutdown', close_mongo_connection)

app.include_router(liker, prefix='/api/v1/likes', tags=['Likes'])
app.include_router(reviewer, prefix='/api/v1/reviews', tags=['Reviews'])
app.include_router(favoriter, prefix='/api/v1/favorites', tags=['Favorites'])
app.include_router(auther, prefix='/api/v1/auth', tags=['Auth'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=os.getenv('LIKE_SERVICE_HOST'),
        port=os.getenv('LIKE_SERVICE_PORT'),
    )
