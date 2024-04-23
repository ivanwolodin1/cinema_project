from pydantic import BaseModel


class AuthTokens(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
