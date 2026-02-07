"""
FastAPI Main Application
AI Meme Generator - Orchestrates the meme generation pipeline
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from datetime import datetime

from app.news_scraper import NewsScraperService
from app.meme_creator import MemeCreatorService
from app.text_generator import MemeTextGenerator
from app.social_poster import SocialMediaPoster
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Meme Generator",
    description="Generate viral memes from trending news headlines using AI",
    version="1.0.0"
)

# Response models
class Meme(BaseModel):
    headline: str
    meme_text_top: str
    meme_text_bottom: str
    template_name: str
    image_url: str
    created_at: str

class MemeResponse(BaseModel):
    status: str
    memes: List[Meme]
    generated_at: str
    count: int

class PostResponse(BaseModel):
    status: str
    platform: str
    post_url: Optional[str]
    message: str

@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {
        "message": "AI Meme Generator API",
        "status": "running",
        "endpoints": {
            "generate": "/generate-memes",
            "templates": "/meme-templates",
            "post": "/post-meme",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "imgflip_configured": bool(settings.IMGFLIP_USERNAME and settings.IMGFLIP_PASSWORD)
    }

@app.get("/meme-templates")
async def get_meme_templates():
    """
    Get list of available meme templates
    
    Returns:
        List of meme templates with IDs and names
    """
    try:
        logger.info("Fetching available meme templates")
        
        meme_creator = MemeCreatorService()
        templates = meme_creator.get_popular_templates()
        
        return {
            "status": "success",
            "templates": templates,
            "count": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch templates: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch templates: {str(e)}"
        )

@app.post("/generate-memes", response_model=MemeResponse)
async def generate_memes(
    num_memes: int = 5,
    news_category: Optional[str] = None
):
    """
    Main endpoint: Generate AI memes from trending news
    
    Process:
    1. Scrape trending news headlines
    2. Use GPT-4 to generate funny meme text
    3. Create meme images with Imgflip API
    4. Return meme URLs
    
    Args:
        num_memes: Number of memes to generate (1-10)
        news_category: Optional news category filter
        
    Returns:
        MemeResponse: Contains generated memes with URLs
    """
    try:
        # Validate input
        if num_memes < 1 or num_memes > 10:
            raise HTTPException(
                status_code=400,
                detail="num_memes must be between 1 and 10"
            )
        
        logger.info(f"Starting meme generation pipeline for {num_memes} memes")
        
        # Step 1: Scrape news headlines
        logger.info("Step 1: Scraping trending news headlines...")
        scraper = NewsScraperService()
        headlines = scraper.get_trending_headlines(
            count=num_memes,
            category=news_category
        )
        
        if not headlines:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch news headlines. Please try again."
            )
        
        logger.info(f"Successfully scraped {len(headlines)} headlines")
        
        # Step 2: Generate meme text for each headline
        logger.info("Step 2: Generating meme text with GPT-4...")
        text_generator = MemeTextGenerator()
        meme_ideas = []
        
        for headline in headlines:
            try:
                meme_text = text_generator.generate_meme_text(headline)
                meme_ideas.append({
                    'headline': headline,
                    'top_text': meme_text['top_text'],
                    'bottom_text': meme_text['bottom_text'],
                    'template_name': meme_text['template_name']
                })
            except Exception as e:
                logger.warning(f"Failed to generate meme for headline: {str(e)}")
                continue
        
        if not meme_ideas:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate meme text. Please check API credentials."
            )
        
        logger.info(f"Successfully generated {len(meme_ideas)} meme ideas")
        
        # Step 3: Create meme images
        logger.info("Step 3: Creating meme images...")
        meme_creator = MemeCreatorService()
        created_memes = []
        
        for idea in meme_ideas:
            try:
                meme_url = meme_creator.create_meme(
                    template_name=idea['template_name'],
                    top_text=idea['top_text'],
                    bottom_text=idea['bottom_text']
                )
                
                created_memes.append(Meme(
                    headline=idea['headline'],
                    meme_text_top=idea['top_text'],
                    meme_text_bottom=idea['bottom_text'],
                    template_name=idea['template_name'],
                    image_url=meme_url,
                    created_at=datetime.utcnow().isoformat()
                ))
                
                logger.info(f"Created meme: {idea['template_name']}")
                
            except Exception as e:
                logger.warning(f"Failed to create meme image: {str(e)}")
                continue
        
        if not created_memes:
            raise HTTPException(
                status_code=500,
                detail="Failed to create meme images. Please check Imgflip credentials."
            )
        
        logger.info(f"Successfully created {len(created_memes)} memes")
        
        # Prepare response
        response = MemeResponse(
            status="success",
            memes=created_memes,
            generated_at=datetime.utcnow().isoformat(),
            count=len(created_memes)
        )
        
        logger.info("Pipeline completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/post-meme")
async def post_meme_to_social(
    meme_url: str,
    caption: str,
    platform: str = "twitter"
):
    """
    Post a meme to social media platforms
    
    Args:
        meme_url: URL of the meme image
        caption: Caption/text for the post
        platform: Social platform (twitter, reddit)
        
    Returns:
        PostResponse: Status and post URL
    """
    try:
        logger.info(f"Posting meme to {platform}")
        
        if platform not in ["twitter", "reddit"]:
            raise HTTPException(
                status_code=400,
                detail="Platform must be 'twitter' or 'reddit'"
            )
        
        poster = SocialMediaPoster()
        
        if platform == "twitter":
            result = poster.post_to_twitter(meme_url, caption)
        else:
            result = poster.post_to_reddit(meme_url, caption)
        
        return PostResponse(
            status="success" if result['success'] else "failed",
            platform=platform,
            post_url=result.get('url'),
            message=result.get('message', '')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to post meme: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to post meme: {str(e)}"
        )

@app.get("/test-components")
async def test_components():
    """
    Test endpoint to verify all components are configured correctly
    """
    results = {
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "imgflip_configured": bool(settings.IMGFLIP_USERNAME and settings.IMGFLIP_PASSWORD),
        "twitter_configured": bool(settings.TWITTER_API_KEY and settings.TWITTER_API_SECRET),
        "reddit_configured": bool(settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET),
        "news_scraper_ready": True
    }
    
    return {
        "status": "component_check",
        "results": results,
        "required_for_memes": {
            "openai": results["openai_configured"],
            "imgflip": results["imgflip_configured"]
        },
        "optional_for_posting": {
            "twitter": results["twitter_configured"],
            "reddit": results["reddit_configured"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)