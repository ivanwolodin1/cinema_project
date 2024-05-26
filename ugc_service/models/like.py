import uuid
from pydantic import BaseModel


class LikeData(BaseModel):
    movie_id: uuid.UUID

