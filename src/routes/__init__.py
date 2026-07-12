"""API Routes Package."""

from src.routes.seo import router as seo_router
from src.routes.contact import router as contact_router

__all__ = ["seo_router", "contact_router"]
