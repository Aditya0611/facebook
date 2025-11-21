#!/usr/bin/env python3
"""
Perfect Facebook Scraper
========================

Production-ready Facebook scraper using free API (facebook-scraper).
Optimized for accuracy, reliability, and data quality.

Features:
- Advanced error handling and retry logic
- Smart hashtag extraction and filtering
- Enhanced engagement metrics calculation
- Sophisticated trending score algorithm
- Data validation and quality checks
- Rate limiting and throttling
- Comprehensive logging

Usage:
------
    from perfect_scraper import PerfectFacebookScraper
    
    scraper = PerfectFacebookScraper()
    results = scraper.get_trending_hashtags('technology', max_posts=100)
"""

import os
import sys
import json
import time
import re
import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from collections import Counter, defaultdict
import logging
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential

# Try to import required libraries
FACEBOOK_SCRAPER_AVAILABLE = False
try:
    from facebook_scraper import get_posts, get_profile
    FACEBOOK_SCRAPER_AVAILABLE = True
except Exception as e:
    # Try importing again - sometimes it works on second try
    try:
        import sys
        # Clear any cached import errors
        if 'facebook_scraper' in sys.modules:
            del sys.modules['facebook_scraper']
        from facebook_scraper import get_posts, get_profile
        FACEBOOK_SCRAPER_AVAILABLE = True
    except:
        import_error = str(e)
        if "No module named 'facebook_scraper'" in import_error or "No module named \"facebook_scraper\"" in import_error:
            print("ERROR: facebook-scraper not installed. Install with: pip install facebook-scraper")
        else:
            # It might still work despite dependency warnings
            print(f"WARNING: facebook-scraper import issue: {e}")
            print("Note: Dependency conflicts may occur but facebook-scraper might still work.")
            print("Try running the script anyway - it may work despite warnings.")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("WARNING: TextBlob not available. Sentiment analysis will be limited.")

from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# RETRY DECORATORS
# ============================================================================

def retry_on_failure(max_attempts=3, delay=2):
    """Retry decorator for API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator


# ============================================================================
# PERFECT FACEBOOK SCRAPER
# ============================================================================

class PerfectFacebookScraper:
    """
    Production-ready Facebook scraper with perfect data quality.
    Uses facebook-scraper library (completely free, unlimited).
    """
    
    # Category keywords for better search
    CATEGORY_KEYWORDS = {
        'technology': ['technology', 'tech', 'AI', 'artificial intelligence', 'software', 'coding', 
                      'programming', 'developer', 'innovation', 'startup tech'],
        'business': ['business', 'entrepreneur', 'startup', 'marketing', 'finance', 'investment',
                    'commerce', 'corporate', 'enterprise'],
        'health': ['health', 'fitness', 'wellness', 'nutrition', 'medical', 'healthcare',
                  'exercise', 'diet', 'mental health'],
        'food': ['food', 'recipe', 'cooking', 'restaurant', 'cuisine', 'culinary',
                'dining', 'chef', 'gastronomy'],
        'travel': ['travel', 'tourism', 'vacation', 'adventure', 'explore', 'journey',
                  'destination', 'wanderlust'],
        'fashion': ['fashion', 'style', 'clothing', 'outfit', 'trend', 'designer',
                   'apparel', 'wardrobe'],
        'entertainment': ['entertainment', 'movie', 'music', 'celebrity', 'show', 'film',
                         'actor', 'singer', 'artist'],
        'sports': ['sports', 'athlete', 'game', 'match', 'championship', 'team',
                  'player', 'competition']
    }
    
    # Common words to filter out
    STOP_WORDS = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
        'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
        'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
        'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its',
        'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our',
        'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any',
        'these', 'give', 'day', 'most', 'us'
    }
    
    def __init__(self, cookies: Optional[str] = None, debug: bool = False):
        """
        Initialize perfect Facebook scraper.
        
        Args:
            cookies: Optional cookies file path for better access
            debug: Enable debug logging
        """
        if not FACEBOOK_SCRAPER_AVAILABLE:
            raise ImportError(
                "facebook-scraper not installed. "
                "Install with: pip install facebook-scraper"
            )
        
        self.cookies = cookies or os.getenv('FACEBOOK_COOKIES_FILE')
        self.debug = debug
        
        # Check if cookies file exists
        self.cookies_available = False
        if self.cookies:
            cookies_path = Path(self.cookies)
            if cookies_path.exists():
                self.cookies_available = True
                self.logger.info(f"Cookies file found: {self.cookies}")
            else:
                self.logger.warning(f"Cookies file specified but not found: {self.cookies}")
        else:
            self.logger.warning(
                "No cookies file configured. Facebook requires cookies for most content. "
                "Set FACEBOOK_COOKIES_FILE in .env or pass cookies parameter. "
                "See HOW_TO_USE_COOKIES.md for instructions."
            )
        
        # Setup logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.stats = {
            'total_posts_scraped': 0,
            'total_hashtags_found': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': datetime.now()
        }
        
        self.logger.info("PerfectFacebookScraper initialized")
    
    @retry_on_failure(max_attempts=3, delay=2)
    def _get_posts_safe(self, keyword: str, pages: int = 5) -> List[Dict]:
        """
        Safely get posts with error handling and retry logic.
        Uses multiple strategies for maximum reliability.
        
        Args:
            keyword: Search keyword
            pages: Number of pages to scrape
            
        Returns:
            List of post dictionaries
        """
        posts = []
        options = {
            'posts_per_page': 25,
            'cookies': self.cookies,
            'timeout': 60,
            'extra_info': True
        }
        
        # Strategy 1: Try popular pages first (most reliable without cookies)
        # Page names work better than URLs
        popular_pages = self._get_popular_pages_for_keyword(keyword)
        if popular_pages:
            for page_name in popular_pages[:3]:  # Try top 3 pages
                try:
                    self.logger.debug(f"Trying page: {page_name}")
                    # Use page name directly (not URL)
                    for post in get_posts(page_name, pages=min(pages, 3), options=options):
                        if self._validate_post(post):
                            posts.append(self._normalize_post(post))
                        if len(posts) >= pages * 25:
                            break
                    if posts:
                        self.logger.info(f"Found {len(posts)} posts from page: {page_name}")
                        self.stats['successful_requests'] += 1
                        self.stats['total_posts_scraped'] += len(posts)
                        return posts
                except Exception as e:
                    self.logger.debug(f"Page {page_name} failed: {e}")
                    continue
        
        # Strategy 2: Try hashtag using page format (hashtag as page name)
        hashtag_keyword = keyword.replace(' ', '').lower()
        # Validate keyword is not empty or invalid
        if hashtag_keyword and len(hashtag_keyword) >= 2 and hashtag_keyword.replace('_', '').isalnum():
            try:
                # Try using hashtag as page identifier
                self.logger.debug(f"Trying hashtag as page: {hashtag_keyword}")
                for post in get_posts(hashtag_keyword, pages=min(pages, 2), options=options):
                    if self._validate_post(post):
                        posts.append(self._normalize_post(post))
                    if len(posts) >= pages * 25:
                        break
                if posts:
                    self.logger.info(f"Found {len(posts)} posts from hashtag")
                    self.stats['successful_requests'] += 1
                    self.stats['total_posts_scraped'] += len(posts)
                    return posts
            except Exception as e:
                self.logger.debug(f"Hashtag as page failed: {e}")
        
        # Strategy 3: Try search (requires cookies, may fail)
        # Validate keyword for search
        if keyword and len(keyword) >= 2:
            # Try different search formats
            search_terms = [
                keyword,
                keyword.replace(' ', '%20'),
                keyword.replace(' ', '+'),
            ]
            
            for search_term in search_terms:
                try:
                    # Try as page name first
                    self.logger.debug(f"Trying search term as page: {search_term}")
                    for post in get_posts(search_term, pages=min(pages, 2), options=options):
                        if self._validate_post(post):
                            posts.append(self._normalize_post(post))
                        if len(posts) >= pages * 25:
                            break
                    if posts:
                        self.logger.info(f"Found {len(posts)} posts from search term")
                        break
                except Exception as e:
                    self.logger.debug(f"Search term failed: {e}")
                    continue
        
        
        if posts:
            self.stats['successful_requests'] += 1
            self.stats['total_posts_scraped'] += len(posts)
        else:
            self.stats['failed_requests'] += 1
            self.logger.warning(f"No posts found for keyword: {keyword}")
            if not self.cookies_available:
                self.logger.warning(
                    "⚠️  No cookies configured! Facebook requires authentication to access content. "
                    "Without cookies, most pages return empty results. "
                    "See HOW_TO_USE_COOKIES.md for instructions on exporting cookies."
                )
        
        return posts
    
    def _get_popular_pages_for_keyword(self, keyword: str) -> List[str]:
        """Get popular Facebook pages for a keyword"""
        page_map = {
            'technology': ['nasa', 'microsoft', 'google', 'techcrunch', 'wired', 'theverge'],
            'tech': ['nasa', 'microsoft', 'google', 'techcrunch', 'wired', 'theverge'],
            'ai': ['openai', 'artificialintelligence', 'machinelearning', 'deeplearning'],
            'artificial intelligence': ['openai', 'artificialintelligence', 'machinelearning'],
            'software': ['microsoft', 'google', 'adobe', 'oracle'],
            'business': ['entrepreneur', 'forbes', 'businessinsider', 'bloomberg'],
            'health': ['who', 'mayoclinic', 'webmd', 'healthline'],
            'food': ['tasty', 'foodnetwork', 'bonappetit', 'buzzfeedfood'],
            'travel': ['lonelyplanet', 'nationalgeographic', 'travelchannel'],
            'fashion': ['vogue', 'elle', 'harpersbazaar', 'instyle'],
            'entertainment': ['entertainment', 'hollywoodreporter', 'variety'],
            'sports': ['espn', 'nba', 'nfl', 'fifa'],
        }
        
        keyword_lower = keyword.lower()
        return page_map.get(keyword_lower, [])
    
    def _validate_post(self, post: Dict) -> bool:
        """Validate post data quality"""
        # Must have text
        if not post.get('text'):
            return False
        
        # Text must be meaningful (at least 10 characters)
        text = post.get('text', '').strip()
        if len(text) < 10:
            return False
        
        # Filter out spam/ads (basic checks)
        spam_indicators = ['click here', 'buy now', 'limited time', 'act now']
        text_lower = text.lower()
        if any(indicator in text_lower for indicator in spam_indicators):
            return False
        
        return True
    
    def _normalize_post(self, post: Dict) -> Dict:
        """Normalize post data structure"""
        # Handle different reaction formats
        reactions = post.get('reactions', {})
        if isinstance(reactions, dict):
            likes = reactions.get('total', 0) or reactions.get('like', 0)
        else:
            likes = post.get('likes', 0) or 0
        
        return {
            'text': post.get('text', '').strip(),
            'post_id': post.get('post_id', ''),
            'time': post.get('time'),
            'likes': int(likes) if likes else 0,
            'comments': int(post.get('comments', 0)) if post.get('comments') else 0,
            'shares': int(post.get('shares', 0)) if post.get('shares') else 0,
            'post_url': post.get('post_url', ''),
            'reactions': reactions
        }
    
    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text with quality filtering.
        
        Args:
            text: Post text
            
        Returns:
            List of clean hashtag strings
        """
        # Extract explicit hashtags
        hashtags = re.findall(r'#(\w+)', text)
        
        # Clean and filter
        cleaned = []
        for tag in hashtags:
            tag_lower = tag.lower()
            
            # Filter out stop words
            if tag_lower in self.STOP_WORDS:
                continue
            
            # Filter out too short or too long
            if len(tag) < 2 or len(tag) > 50:
                continue
            
            # Filter out common non-meaningful tags
            if tag_lower in ['like', 'share', 'comment', 'follow', 'subscribe']:
                continue
            
            cleaned.append(tag)
        
        return list(set(cleaned))  # Remove duplicates
    
    def extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """
        Extract meaningful keywords from text.
        
        Args:
            text: Post text
            min_length: Minimum keyword length
            
        Returns:
            List of keyword strings
        """
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = re.findall(r'\b\w+\b', text)
        
        # Filter
        keywords = [
            w for w in words
            if len(w) >= min_length
            and w not in self.STOP_WORDS
            and not w.isdigit()
        ]
        
        # Get most common keywords
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(5) if count >= 2]
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment with enhanced accuracy.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (sentiment_label, polarity_score)
        """
        if not TEXTBLOB_AVAILABLE:
            return "neutral", 0.0
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Enhanced sentiment classification
            if polarity > 0.15:
                sentiment = "positive"
            elif polarity < -0.15:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            # Adjust for subjectivity
            if subjectivity > 0.5:
                # More subjective, adjust polarity
                polarity = polarity * 0.9
            
            return sentiment, round(polarity, 3)
            
        except Exception as e:
            self.logger.debug(f"Sentiment analysis error: {e}")
            return "neutral", 0.0
    
    def calculate_engagement_score(self, likes: int, comments: int, shares: int) -> float:
        """
        Calculate sophisticated engagement score (1-10).
        
        Args:
            likes: Number of likes
            comments: Number of comments
            shares: Number of shares
            
        Returns:
            Engagement score (1.0-10.0)
        """
        # Weighted engagement (comments and shares are more valuable)
        weighted = (likes * 1.0) + (comments * 4.0) + (shares * 8.0)
        
        if weighted == 0:
            return 1.0
        
        # Logarithmic scaling for better distribution
        if weighted <= 20:
            score = 1.0 + (weighted / 20) * 1.5
        elif weighted <= 100:
            score = 2.5 + ((weighted - 20) / 80) * 1.5
        elif weighted <= 500:
            score = 4.0 + ((weighted - 500) / 400) * 2.0
        elif weighted <= 2000:
            score = 6.0 + ((weighted - 500) / 1500) * 2.0
        elif weighted <= 10000:
            score = 8.0 + ((weighted - 2000) / 8000) * 1.5
        else:
            score = min(10.0, 9.5 + (math.log10(weighted) - 4) * 0.125)
        
        return round(max(1.0, min(10.0, score)), 2)
    
    def calculate_trending_score(self, hashtag_data: Dict) -> float:
        """
        Calculate sophisticated trending score (0-100).
        
        Args:
            hashtag_data: Hashtag data dictionary
            
        Returns:
            Trending score (0-100)
        """
        engagement_score = hashtag_data.get('engagement_score', 0)
        post_count = hashtag_data.get('post_count', 0)
        total_engagement = hashtag_data.get('total_engagement', 0)
        avg_engagement = hashtag_data.get('avg_engagement', 0)
        sentiment_score = hashtag_data.get('sentiment_score', 0)
        
        # Normalize metrics
        eng_norm = min(engagement_score / 10.0, 1.0)
        post_norm = min(math.log1p(post_count) / math.log1p(25), 1.0)
        total_norm = min(math.log1p(total_engagement) / math.log1p(25000), 1.0)
        avg_norm = min(math.log1p(avg_engagement) / math.log1p(2500), 1.0)
        sentiment_norm = (sentiment_score + 1) / 2
        
        # Sentiment weighting
        if sentiment_score > 0:
            sentiment_weight = 1.0 + (sentiment_score * 0.3)
        elif sentiment_score < 0:
            sentiment_weight = 1.0 + (sentiment_score * 0.2)
        else:
            sentiment_weight = 1.0
        
        # Calculate base score
        base_score = (
            eng_norm * 0.30 +      # Engagement (30%)
            post_norm * 0.25 +     # Post count (25%)
            total_norm * 0.15 +    # Total engagement (15%)
            avg_norm * 0.15 +      # Average engagement (15%)
            sentiment_norm * 0.15  # Sentiment (15%)
        )
        
        # Apply sentiment weight
        base_score *= sentiment_weight
        
        # Scale to 0-100
        final_score = base_score * 100
        
        return round(min(max(final_score, 0), 100), 2)
    
    def get_trending_hashtags(self, category: str, max_posts: int = 100) -> List[Dict]:
        """
        Get trending hashtags for a category with perfect accuracy.
        
        Args:
            category: Category name
            max_posts: Maximum posts to analyze
            
        Returns:
            List of top trending hashtag dictionaries
        """
        category = category.lower().strip()
        
        # Validate category
        if not category or category == "." or len(category) < 2:
            self.logger.warning(f"Invalid category: '{category}'. Using 'technology' as default.")
            category = "technology"
        
        if category not in self.CATEGORY_KEYWORDS:
            self.logger.warning(f"Unknown category: {category}. Using default keywords.")
            # Only use category as keyword if it's a valid word
            if category and len(category) >= 2 and category.replace(' ', '').isalnum():
                keywords = [category]
            else:
                # Fallback to technology keywords
                self.logger.info("Using 'technology' keywords as fallback")
                keywords = self.CATEGORY_KEYWORDS.get('technology', ['technology'])
        else:
            keywords = self.CATEGORY_KEYWORDS[category]
        
        self.logger.info(f"Scraping trending hashtags for category: {category}")
        self.logger.info(f"Using keywords: {keywords[:5]}")
        
        all_hashtag_data = defaultdict(lambda: {
            'hashtag': '',
            'category': category,
            'post_count': 0,
            'total_engagement': 0,
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'sentiment_scores': [],
            'engagement_scores': [],
            'posts': []
        })
        
        # Scrape posts for each keyword
        posts_per_keyword = max(1, max_posts // len(keywords[:5]))
        
        for i, keyword in enumerate(keywords[:5], 1):
            self.logger.info(f"Processing keyword {i}/{min(5, len(keywords))}: {keyword}")
            
            try:
                pages = max(1, posts_per_keyword // 25)
                posts = self._get_posts_safe(keyword, pages=pages)
                
                if not posts:
                    self.logger.warning(f"No posts found for keyword: {keyword}")
                    continue
                
                self.logger.info(f"Found {len(posts)} posts for '{keyword}'")
                
                # Process each post
                for post in posts:
                    text = post.get('text', '')
                    if not text:
                        continue
                    
                    # Extract hashtags
                    hashtags = self.extract_hashtags(text)
                    
                    # Extract keywords if no hashtags
                    if not hashtags:
                        keywords_from_text = self.extract_keywords(text)
                        hashtags = [kw for kw in keywords_from_text if len(kw) >= 3]
                    
                    if not hashtags:
                        continue
                    
                    # Analyze sentiment
                    sentiment, polarity = self.analyze_sentiment(text)
                    
                    # Get engagement metrics
                    likes = post.get('likes', 0)
                    comments = post.get('comments', 0)
                    shares = post.get('shares', 0)
                    engagement = likes + comments + shares
                    
                    # Calculate engagement score
                    engagement_score = self.calculate_engagement_score(likes, comments, shares)
                    
                    # Process each hashtag
                    for tag in hashtags:
                        tag_lower = tag.lower()
                        tag_data = all_hashtag_data[tag_lower]
                        
                        # Initialize if new
                        if not tag_data['hashtag']:
                            tag_data['hashtag'] = tag
                        
                        # Update metrics
                        tag_data['post_count'] += 1
                        tag_data['total_engagement'] += engagement
                        tag_data['likes'] += likes
                        tag_data['comments'] += comments
                        tag_data['shares'] += shares
                        tag_data['sentiment_scores'].append(polarity)
                        tag_data['engagement_scores'].append(engagement_score)
                        tag_data['posts'].append({
                            'text': text[:200],  # Store preview
                            'engagement': engagement,
                            'sentiment': sentiment
                        })
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Error processing keyword '{keyword}': {e}")
                continue
        
        # Calculate final metrics
        results = []
        for tag_data in all_hashtag_data.values():
            if tag_data['post_count'] < 2:  # Filter out single-post hashtags
                continue
            
            count = tag_data['post_count']
            
            # Calculate averages
            tag_data['avg_engagement'] = tag_data['total_engagement'] / count
            tag_data['avg_likes'] = tag_data['likes'] / count
            tag_data['avg_comments'] = tag_data['comments'] / count
            tag_data['avg_shares'] = tag_data['shares'] / count
            
            # Calculate average sentiment
            sentiment_scores = tag_data['sentiment_scores']
            tag_data['sentiment_score'] = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
            
            # Determine sentiment label
            if tag_data['sentiment_score'] > 0.1:
                tag_data['sentiment'] = 'positive'
            elif tag_data['sentiment_score'] < -0.1:
                tag_data['sentiment'] = 'negative'
            else:
                tag_data['sentiment'] = 'neutral'
            
            # Calculate engagement score (average of all posts)
            engagement_scores = tag_data['engagement_scores']
            tag_data['engagement_score'] = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 1.0
            
            # Calculate trending score
            tag_data['trending_score'] = self.calculate_trending_score(tag_data)
            
            # Clean up temporary fields
            tag_data.pop('sentiment_scores', None)
            tag_data.pop('engagement_scores', None)
            tag_data.pop('posts', None)
            
            results.append(tag_data)
        
        # Sort by trending score
        results.sort(key=lambda x: x['trending_score'], reverse=True)
        
        self.stats['total_hashtags_found'] += len(results)
        
        self.logger.info(f"Found {len(results)} unique hashtags (filtered from {len(all_hashtag_data)} total)")
        
        return results[:10]  # Return top 10
    
    def save_results(self, results: List[Dict], category: str, filename: Optional[str] = None):
        """Save results to JSON file with metadata"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/perfect_scraper_{category}_{timestamp}.json"
        
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        output = {
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'count': len(results),
            'stats': {
                'total_posts_scraped': self.stats['total_posts_scraped'],
                'successful_requests': self.stats['successful_requests'],
                'failed_requests': self.stats['failed_requests'],
                'scraping_duration': str(datetime.now() - self.stats['start_time'])
            },
            'trends': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"Results saved to {filepath}")
        return filepath
    
    def get_stats(self) -> Dict:
        """Get scraping statistics"""
        duration = datetime.now() - self.stats['start_time']
        return {
            **self.stats,
            'duration_seconds': duration.total_seconds(),
            'success_rate': (
                self.stats['successful_requests'] / 
                max(self.stats['successful_requests'] + self.stats['failed_requests'], 1) * 100
            )
        }


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_perfect_scraper(cookies: Optional[str] = None, debug: bool = False):
    """
    Factory function to create perfect scraper.
    
    Args:
        cookies: Optional cookies file path
        debug: Enable debug logging
        
    Returns:
        PerfectFacebookScraper instance
    """
    return PerfectFacebookScraper(cookies=cookies, debug=debug)

