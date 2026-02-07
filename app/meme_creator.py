"""
Meme Creator Service
Creates meme images using Imgflip API
"""

import requests
import logging
from typing import Dict, List
from app.config import settings

logger = logging.getLogger(__name__)

class MemeCreatorService:
    """
    Creates meme images using Imgflip API
    """
    
    def __init__(self):
        """
        Initialize Imgflip service
        """
        self.username = settings.IMGFLIP_USERNAME
        self.password = settings.IMGFLIP_PASSWORD
        self.base_url = settings.IMGFLIP_API_URL
        self.templates = settings.DEFAULT_MEME_TEMPLATES
        logger.info("Initialized MemeCreatorService with Imgflip")
    
    def create_meme(
        self,
        template_name: str,
        top_text: str,
        bottom_text: str
    ) -> str:
        """
        Create a meme image
        
        Args:
            template_name: Name of meme template
            top_text: Text for top of meme
            bottom_text: Text for bottom of meme
            
        Returns:
            URL of created meme image
        """
        try:
            # Get template ID
            template_id = self.templates.get(template_name)
            
            if not template_id:
                logger.warning(f"Template '{template_name}' not found, using default")
                template_id = self.templates['Drake Hotline Bling']
            
            logger.info(f"Creating meme with template: {template_name} (ID: {template_id})")
            
            # Prepare request
            url = f"{self.base_url}/caption_image"
            
            data = {
                'template_id': template_id,
                'username': self.username,
                'password': self.password,
                'text0': top_text,
                'text1': bottom_text
            }
            
            # Make request
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                error_msg = result.get('error_message', 'Unknown error')
                raise ValueError(f"Imgflip API error: {error_msg}")
            
            meme_url = result['data']['url']
            logger.info(f"Meme created successfully: {meme_url}")
            
            return meme_url
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error creating meme: {str(e)}")
            raise ValueError(f"Failed to create meme: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error creating meme: {str(e)}")
            raise ValueError(f"Failed to create meme: {str(e)}")
    
    def get_popular_templates(self) -> List[Dict[str, str]]:
        """
        Get list of popular meme templates
        
        Returns:
            List of template dictionaries
        """
        try:
            url = f"{self.base_url}/get_memes"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                logger.warning("Failed to fetch templates from API, using defaults")
                return self._get_default_templates()
            
            # Get top 100 memes
            all_memes = result['data']['memes']
            
            # Filter to our popular ones
            popular = []
            for name, template_id in self.templates.items():
                # Find in API results
                matching = [m for m in all_memes if m['id'] == template_id]
                if matching:
                    meme = matching[0]
                    popular.append({
                        'id': meme['id'],
                        'name': meme['name'],
                        'url': meme['url'],
                        'width': meme['width'],
                        'height': meme['height'],
                        'box_count': meme['box_count']
                    })
            
            logger.info(f"Fetched {len(popular)} popular templates")
            return popular
            
        except Exception as e:
            logger.error(f"Error fetching templates: {str(e)}")
            return self._get_default_templates()
    
    def _get_default_templates(self) -> List[Dict[str, str]]:
        """
        Get default template list (fallback)
        
        Returns:
            List of default templates
        """
        return [
            {
                'id': template_id,
                'name': name,
                'url': f'https://imgflip.com/s/meme/{template_id}.jpg',
                'box_count': 2
            }
            for name, template_id in self.templates.items()
        ]
    
    def test_connection(self) -> bool:
        """
        Test Imgflip API connection and credentials
        
        Returns:
            True if connection successful
        """
        try:
            # Try to get memes (doesn't require auth)
            url = f"{self.base_url}/get_memes"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('success'):
                logger.info("Imgflip API connection successful")
                return True
            else:
                logger.error("Imgflip API returned error")
                return False
                
        except Exception as e:
            logger.error(f"Imgflip connection test failed: {str(e)}")
            return False
    
    def create_custom_meme(
        self,
        template_id: str,
        texts: List[str]
    ) -> str:
        """
        Create meme with custom template and multiple text boxes
        
        Args:
            template_id: Imgflip template ID
            texts: List of text for each box
            
        Returns:
            URL of created meme
        """
        try:
            url = f"{self.base_url}/caption_image"
            
            data = {
                'template_id': template_id,
                'username': self.username,
                'password': self.password,
            }
            
            # Add text boxes
            for i, text in enumerate(texts):
                data[f'boxes[{i}][text]'] = text
            
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise ValueError(f"API error: {result.get('error_message')}")
            
            return result['data']['url']
            
        except Exception as e:
            logger.error(f"Error creating custom meme: {str(e)}")
            raise