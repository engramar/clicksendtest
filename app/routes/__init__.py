"""Route definitions."""
from fastapi import APIRouter
from app.routes import api_routes

router = APIRouter()
router.include_router(api_routes.router, prefix="/api", tags=["api"])

__all__ = ["router"]

