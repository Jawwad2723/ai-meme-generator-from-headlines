"""
Configuration Module
Manages environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # OpenAI Configuration (Required)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Imgflip Configuration (Required - for meme generation)
    IMGFLIP_USERNAME: str = os.getenv("IMGFLIP_USERNAME", "")
    IMGFLIP_PASSWORD: str = os.getenv("IMGFLIP_PASSWORD", "")
    IMGFLIP_API_URL: str = "https://api.imgflip.com"
    
    # Twitter API Configuration (Optional - for posting)
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_SECRET: str = os.getenv("TWITTER_ACCESS_SECRET", "")
    
    # Reddit API Configuration (Optional - for posting)
    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USERNAME: str = os.getenv("REDDIT_USERNAME", "")
    REDDIT_PASSWORD: str = os.getenv("REDDIT_PASSWORD", "")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "AI Meme Generator Bot 1.0")
    
    # News Sources Configuration
    NEWS_SOURCES: list = [
        "https://www.bbc.com/news",
        "https://techcrunch.com",
        "https://www.theverge.com",
        "https://arstechnica.com",
        "https://www.reuters.com/technology",
        "https://apnews.com",
        "https://www.theguardian.com/international",
        "https://www.cnbc.com",
    ]
    
    # Meme Templates (Most Popular)
    DEFAULT_MEME_TEMPLATES: dict = {
        "Distracted Boyfriend": "112126428",
        "Drake Hotline Bling": "181913649",
        "Two Buttons": "87743020",
        "Expanding Brain": "93895088",
        "Change My Mind": "129242436",
        "Is This A Pigeon": "100947",
        "Woman Yelling At Cat": "188390779",
        "Success Kid": "61544",
        "One Does Not Simply": "61579",
        "Ancient Aliens": "101470"
    }
    
    # User Agent for web scraping
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Request timeout in seconds
    REQUEST_TIMEOUT: int = 30
    
    # Application Settings
    APP_NAME: str = "AI Meme Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Rate Limiting
    MAX_MEMES_PER_REQUEST: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Validation function
def validate_settings():
    """
    Validate that required settings are configured
    """
    errors = []
    
    if not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set (Required for meme text generation)")
    
    if not settings.IMGFLIP_USERNAME or not settings.IMGFLIP_PASSWORD:
        errors.append("IMGFLIP credentials are not set (Required for meme image creation)")
    
    if errors:
        error_message = "Configuration errors:\n" + "\n".join(f"- {error}" for error in errors)
        raise ValueError(error_message)
    
    return True

# Run validation on import if not in debug mode
if not settings.DEBUG:
    # Comment out for initial setup, uncomment for production
    pass  # validate_settings()