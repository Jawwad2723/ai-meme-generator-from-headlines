"""
News Scraper Service
Scrapes trending news headlines from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional
from datetime import datetime
import time
from app.config import settings

logger = logging.getLogger(__name__)

class NewsScraperService:
    """
    Scrapes trending news headlines for meme generation
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': settings.USER_AGENT
        }
        self.timeout = settings.REQUEST_TIMEOUT
    
    def get_trending_headlines(
        self, 
        count: int = 5,
        category: Optional[str] = None
    ) -> List[str]:
        """
        Get trending news headlines
        
        Args:
            count: Number of headlines to fetch
            category: Optional category filter
            
        Returns:
            List of headline strings
        """
        headlines = []
        sources_tried = 0
        max_sources = len(settings.NEWS_SOURCES)
        
        logger.info(f"Starting to scrape {count} headlines")
        
        # Try different sources until we get enough headlines
        for source_url in settings.NEWS_SOURCES:
            if len(headlines) >= count:
                break
            
            sources_tried += 1
            logger.info(f"Trying source {sources_tried}/{max_sources}: {source_url}")
            
            try:
                source_headlines = self._scrape_from_source(source_url)
                headlines.extend(source_headlines)
                
                # Small delay to be respectful
                time.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"Failed to scrape from {source_url}: {str(e)}")
                continue
        
        # Remove duplicates while preserving order
        unique_headlines = []
        seen = set()
        for h in headlines:
            if h.lower() not in seen:
                seen.add(h.lower())
                unique_headlines.append(h)
        
        logger.info(f"Successfully scraped {len(unique_headlines)} unique headlines from {sources_tried} sources")
        return unique_headlines[:count]
    
    def _scrape_from_source(self, url: str) -> List[str]:
        """
        Scrape headlines from a single news source
        
        Args:
            url: News source URL
            
        Returns:
            List of headlines
        """
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Common headline selectors (try multiple)
            selectors = [
                'h1', 'h2', 'h3',
                '.headline', '.title',
                '[class*="headline"]', '[class*="title"]',
                'article h2', 'article h3'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    
                    # Filter valid headlines
                    if self._is_valid_headline(text):
                        headlines.append(text)
                        
                        if len(headlines) >= 20:  # Get up to 20 from each source
                            break
                
                if headlines:
                    break
            
            logger.info(f"Found {len(headlines)} headlines from {url}")
            return headlines
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []
    
    def _is_valid_headline(self, text: str) -> bool:
        """
        Validate if text is a good headline for memes
        
        Args:
            text: Headline text
            
        Returns:
            True if valid, False otherwise
        """
        # Check length
        if len(text) < 20 or len(text) > 200:
            return False
        
        # Must have alphabetic characters
        if not any(c.isalpha() for c in text):
            return False
        
        # Filter out common non-headlines
        ignore_phrases = [
            'subscribe', 'newsletter', 'sign up', 'cookie',
            'privacy policy', 'terms of service', 'advertisement',
            'sponsored', 'shop now', 'buy now', 'click here'
        ]
        
        text_lower = text.lower()
        if any(phrase in text_lower for phrase in ignore_phrases):
            return False
        
        # Should look like news
        # (has some capitalization, punctuation, etc.)
        if text.isupper() or text.islower():
            return False
        
        return True
    
    def get_headline_by_category(self, category: str) -> List[str]:
        """
        Get headlines from specific category
        
        Args:
            category: News category (tech, business, sports, etc.)
            
        Returns:
            List of headlines
        """
        # Category-specific sources
        category_sources = {
            'tech': [
                "https://techcrunch.com",
                "https://www.theverge.com",
                "https://arstechnica.com"
            ],
            'business': [
                "https://www.cnbc.com",
                "https://www.bloomberg.com"
            ],
            'sports': [
                "https://www.espn.com",
                "https://www.bbc.com/sport"
            ]
        }
        
        sources = category_sources.get(category.lower(), settings.NEWS_SOURCES)
        
        headlines = []
        for source in sources[:3]:  # Try up to 3 sources per category
            try:
                source_headlines = self._scrape_from_source(source)
                headlines.extend(source_headlines)
            except:
                continue
        
        return headlines[:10]