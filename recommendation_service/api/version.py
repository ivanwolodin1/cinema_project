"""Endpoints for getting version information."""
from typing import Any
from fastapi import APIRouter
from ..schemas.version import VersionResponse
from ..version import __version__

version_router = APIRouter()


@version_router.get("/version", response_model=VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return VersionResponse(version=__version__)
