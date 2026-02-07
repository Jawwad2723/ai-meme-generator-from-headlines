"""
Meme Text Generator
Uses OpenAI GPT-4 to generate funny meme text from news headlines
"""

from openai import OpenAI
import logging
import json
from typing import Dict
from app.config import settings

logger = logging.getLogger(__name__)

class MemeTextGenerator:
    """
    Generates meme text using OpenAI GPT-4
    """
    
    def __init__(self):
        """
        Initialize OpenAI client
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.templates = settings.DEFAULT_MEME_TEMPLATES
        logger.info(f"Initialized MemeTextGenerator with model: {self.model}")
    
    def generate_meme_text(self, headline: str) -> Dict[str, str]:
        """
        Generate meme text from a news headline
        
        Args:
            headline: News headline
            
        Returns:
            Dictionary with top_text, bottom_text, and template_name
        """
        try:
            logger.info(f"Generating meme for headline: {headline[:60]}...")
            
            # Create the prompt
            prompt = self._create_meme_prompt(headline)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a viral meme creator. You take news headlines and turn them "
                            "into funny, relatable memes. Your memes are witty, use internet humor, "
                            "and are appropriate for general audiences (PG-13). You understand meme "
                            "formats and how to match headlines to the right templates."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Higher creativity for humor
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Validate and clean
            meme_data = {
                'top_text': result.get('top_text', '').upper(),
                'bottom_text': result.get('bottom_text', '').upper(),
                'template_name': result.get('template_name', 'Drake Hotline Bling')
            }
            
            # Ensure template exists
            if meme_data['template_name'] not in self.templates:
                meme_data['template_name'] = 'Drake Hotline Bling'
            
            logger.info(f"Generated meme: {meme_data['template_name']}")
            return meme_data
            
        except Exception as e:
            logger.error(f"Error generating meme text: {str(e)}")
            # Fallback to simple meme
            return self._create_fallback_meme(headline)
    
    def _create_meme_prompt(self, headline: str) -> str:
        """
        Create prompt for GPT-4
        
        Args:
            headline: News headline
            
        Returns:
            Formatted prompt
        """
        template_list = ", ".join(self.templates.keys())
        
        prompt = f"""
Create a funny meme from this news headline:
"{headline}"

Available meme templates:
{template_list}

IMPORTANT: Your response must be valid JSON with this exact structure:
{{
    "top_text": "text for top of meme (short, punchy, all caps)",
    "bottom_text": "text for bottom of meme (punchline, all caps)",
    "template_name": "exact template name from the list above"
}}

Rules:
1. Make it funny and relatable
2. Use internet humor and meme culture references
3. Keep text SHORT (max 10 words per line)
4. Choose the template that best fits the joke
5. Make the bottom text the punchline
6. Keep it PG-13 appropriate
7. Use ALL CAPS for meme text
8. Be creative and witty

Example for headline "Tech CEO Says AI Will Replace All Jobs":
{{
    "top_text": "TECH CEO: AI WILL REPLACE ALL JOBS",
    "bottom_text": "ALSO TECH CEO: WHY IS NOBODY BUYING OUR PRODUCTS",
    "template_name": "Drake Hotline Bling"
}}

Now create a meme for the headline above. Respond ONLY with valid JSON.
"""
        return prompt
    
    def _create_fallback_meme(self, headline: str) -> Dict[str, str]:
        """
        Create a simple fallback meme if GPT-4 fails
        
        Args:
            headline: News headline
            
        Returns:
            Basic meme data
        """
        # Simple extraction: first part as top, "meanwhile..." as bottom
        words = headline.split()
        
        if len(words) > 8:
            top_text = " ".join(words[:8]).upper()
            bottom_text = "MEANWHILE IN 2024..."
        else:
            top_text = headline.upper()
            bottom_text = "NOBODY SAW THAT COMING"
        
        return {
            'top_text': top_text,
            'bottom_text': bottom_text,
            'template_name': 'Drake Hotline Bling'
        }
    
    def generate_caption(self, headline: str, meme_text: Dict[str, str]) -> str:
        """
        Generate a social media caption for the meme
        
        Args:
            headline: Original headline
            meme_text: Generated meme text
            
        Returns:
            Caption text
        """
        try:
            prompt = f"""
Create a short, witty social media caption for this meme:

Original headline: {headline}
Meme top text: {meme_text['top_text']}
Meme bottom text: {meme_text['bottom_text']}

The caption should:
- Be 1-2 sentences max
- Be funny and engaging
- Include 2-3 relevant hashtags
- Encourage sharing

Respond with ONLY the caption text, nothing else.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You create viral social media captions for memes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=100
            )
            
            caption = response.choices[0].message.content.strip()
            return caption
            
        except Exception as e:
            logger.error(f"Failed to generate caption: {str(e)}")
            return f"When the news hits different 😂 #{headline.split()[0]} #meme #funny"