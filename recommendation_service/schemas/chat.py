"""Define response model for the endpoint version."""
from pydantic import BaseModel, Field  # type: ignore


class ChatResponse(BaseModel):
    """Response for version endpoint."""
    response: str = Field(...)
