from uuid import UUID
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db.models.recommendation import Recommendation
from ..db.session import SessionLocal, session_scope


class RecommendationService:
    # def __init__(self, session: Session):
    #     self.db = session

    async def get_recommendations(self, user_id: UUID) -> Recommendation:
        with session_scope() as session:
            res = session.scalars(
                select(
                    Recommendation
                ).where(Recommendation.user_id == user_id)).one()
            session.expunge(res)
            return res


@lru_cache()
def get_rec_service() -> RecommendationService:
    return RecommendationService()
