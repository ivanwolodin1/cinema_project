"""The main APIRouter is defined to include all the sub routers from each
module inside the API folder"""
from fastapi import APIRouter
from .version import version_router
from .chat import chat_router
from .recomendation import recommendation_router

api_router = APIRouter()
api_router.include_router(version_router, tags=["version"])
api_router.include_router(chat_router, tags=["version"])
api_router.include_router(recommendation_router, tags=["version"])
