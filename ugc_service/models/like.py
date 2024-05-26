from pydantic import BaseModel


class LikeData(BaseModel):
    movie_id: int
