from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.post import router as post_router


api_router = APIRouter()

# example include router
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(post_router, prefix="/post", tags=["post"])
