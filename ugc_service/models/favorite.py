from pydantic import BaseModel


class BookmarkData(BaseModel):
    movie_id: int
