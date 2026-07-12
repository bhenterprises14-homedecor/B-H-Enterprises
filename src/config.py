"""Application configuration and settings management."""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Site Configuration
    SITE_URL: str = os.getenv("SITE_URL", "https://bhenterprises.com")
    SITE_TITLE: str = "B H Enterprises - Building Materials & Home Decorator"
    SITE_DESCRIPTION: str = (
        "Premium building materials and professional home decorator services in Bangalore. "
        "Quality white cement, putty, paint, and professional painting, carpentry services."
    )
    SITE_KEYWORDS: str = (
        "building materials Bangalore, white cement supplier, home painter, "
        "carpenter services, tile fixing, interior decoration"
    )
    
    # Company Information
    COMPANY_NAME: str = "B H Enterprises"
    GST_NUMBER: str = "07ETTPM3697B1Z4"
    
    # Contact Information
    CONTACT_EMAIL: str = os.getenv("CONTACT_EMAIL", "info@bhenterprises.com")
    CONTACT_PHONE: str = os.getenv("CONTACT_PHONE", "+91-XXXXXXXXXX")
    CONTACT_ADDRESS: str = "Bangalore, India"
    
    # Social Media
    FACEBOOK_URL: str = "https://www.facebook.com/bhenterprises"
    INSTAGRAM_URL: str = "https://www.instagram.com/bhenterprises"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8501",  # Streamlit default port
        "https://bhenterprises.com",
    ]
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
