from pydantic import BaseModel


class ReviewData(BaseModel):
    movie_id: int
    review_text: str
