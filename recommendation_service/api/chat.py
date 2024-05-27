"""Endpoints for getting and posting chat information."""
from fastapi import APIRouter
from ..schemas.chat import ChatResponse

chat_router = APIRouter()


@chat_router.get("/chat", response_model=ChatResponse)
async def chat():
    """Provide version information about the web service.
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return ChatResponse()