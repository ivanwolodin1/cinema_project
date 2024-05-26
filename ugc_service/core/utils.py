import jwt
from core.config import settings


def create_jwt_token(username: str) -> str:
    payload = {'sub': username}
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.HASH_ALGORITHM,
    )
