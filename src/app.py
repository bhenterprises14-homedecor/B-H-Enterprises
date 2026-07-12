"""Main FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from src.config import get_settings
from src.routes import seo_router, contact_router

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="B H Enterprises API",
    description="Building Materials & Home Decorator Services API",
    version="1.0.0",
)

# Get settings
settings = get_settings()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to B H Enterprises API",
        "company": settings.COMPANY_NAME,
        "gst": settings.GST_NUMBER,
        "status": "operational",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }


# Include routers
app.include_router(
    seo_router,
    prefix="/api/seo",
    tags=["SEO"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    contact_router,
    prefix="/api/contact",
    tags=["Contact & Leads"],
    responses={404: {"description": "Not found"}},
)


# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle generic exceptions."""
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on startup."""
    logger.info(
        "app_startup",
        app_name=app.title,
        environment=settings.ENVIRONMENT,
        debug=settings.DEBUG,
    )


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown."""
    logger.info("app_shutdown", app_name=app.title)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
