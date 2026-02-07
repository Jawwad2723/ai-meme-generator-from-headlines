"""
Social Media Poster
Posts memes to Twitter and Reddit (Optional feature)
"""

import logging
from typing import Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class SocialMediaPoster:
    """
    Posts memes to social media platforms
    Note: This is an optional feature requiring additional API keys
    """
    
    def __init__(self):
        """
        Initialize social media clients
        """
        self.twitter_configured = bool(
            settings.TWITTER_API_KEY and 
            settings.TWITTER_API_SECRET
        )
        
        self.reddit_configured = bool(
            settings.REDDIT_CLIENT_ID and 
            settings.REDDIT_CLIENT_SECRET
        )
        
        logger.info(f"Twitter configured: {self.twitter_configured}")
        logger.info(f"Reddit configured: {self.reddit_configured}")
    
    def post_to_twitter(self, image_url: str, caption: str) -> Dict:
        """
        Post meme to Twitter
        
        Args:
            image_url: URL of meme image
            caption: Tweet text
            
        Returns:
            Dictionary with success status and tweet URL
        """
        if not self.twitter_configured:
            return {
                'success': False,
                'message': 'Twitter API not configured. Add credentials to .env file.'
            }
        
        try:
            # Import here to make it optional
            import tweepy
            
            # Authenticate
            auth = tweepy.OAuthHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET
            )
            auth.set_access_token(
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_SECRET
            )
            
            api = tweepy.API(auth)
            
            # Download image
            import requests
            import tempfile
            import os
            
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                tmp.write(response.content)
                tmp_path = tmp.name
            
            try:
                # Upload media
                media = api.media_upload(tmp_path)
                
                # Post tweet
                tweet = api.update_status(
                    status=caption,
                    media_ids=[media.media_id]
                )
                
                tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                
                logger.info(f"Posted to Twitter: {tweet_url}")
                
                return {
                    'success': True,
                    'url': tweet_url,
                    'message': 'Posted successfully to Twitter'
                }
                
            finally:
                # Clean up temp file
                os.unlink(tmp_path)
                
        except ImportError:
            logger.error("tweepy not installed. Install with: pip install tweepy")
            return {
                'success': False,
                'message': 'tweepy library not installed'
            }
        
        except Exception as e:
            logger.error(f"Error posting to Twitter: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def post_to_reddit(
        self, 
        image_url: str, 
        title: str,
        subreddit: str = "memes"
    ) -> Dict:
        """
        Post meme to Reddit
        
        Args:
            image_url: URL of meme image
            title: Post title
            subreddit: Subreddit to post to (default: r/memes)
            
        Returns:
            Dictionary with success status and post URL
        """
        if not self.reddit_configured:
            return {
                'success': False,
                'message': 'Reddit API not configured. Add credentials to .env file.'
            }
        
        try:
            # Import here to make it optional
            import praw
            
            # Authenticate
            reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                username=settings.REDDIT_USERNAME,
                password=settings.REDDIT_PASSWORD,
                user_agent=settings.REDDIT_USER_AGENT
            )
            
            # Submit post
            submission = reddit.subreddit(subreddit).submit(
                title=title,
                url=image_url
            )
            
            post_url = f"https://reddit.com{submission.permalink}"
            
            logger.info(f"Posted to Reddit: {post_url}")
            
            return {
                'success': True,
                'url': post_url,
                'message': f'Posted successfully to r/{subreddit}'
            }
            
        except ImportError:
            logger.error("praw not installed. Install with: pip install praw")
            return {
                'success': False,
                'message': 'praw library not installed'
            }
        
        except Exception as e:
            logger.error(f"Error posting to Reddit: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def is_twitter_configured(self) -> bool:
        """Check if Twitter credentials are set"""
        return self.twitter_configured
    
    def is_reddit_configured(self) -> bool:
        """Check if Reddit credentials are set"""
        return self.reddit_configured