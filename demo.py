#!/usr/bin/env python3
"""
Facebook Scraper Demo Script
Demonstrates the refactored scraper with all improvements:
- Fail-fast imports
- JSON logging
- Config-based categories
- Retry logic
- Enhanced analytics
"""

import sys
import uuid
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from base import FacebookScraper
import logging

def main():
    """Run demo scraping with various categories"""
    
    print("=" * 80)
    print("Facebook Scraper Demo - Production-Ready Version")
    print("=" * 80)
    print()
    
    # Available categories loaded from config/categories.json
    categories = ['technology', 'business', 'health', 'food']
    
    print("Features demonstrated:")
    print("  ✓ Fail-fast imports (no in-process pip install)")
    print("  ✓ JSON structured logging (logs/scraper.log)")
    print("  ✓ Config-based categories (config/categories.json)")
    print("  ✓ Retry logic with exponential backoff")
    print("  ✓ Enhanced analytics:")
    print("    - Time-weighted trend scoring")
    print("    - Sentiment weighting")
    print("    - Engagement normalization")
    print("    - Velocity & consistency metrics")
    print()
    
    category = input(f"Select category {categories}: ").strip().lower()
    
    if category not in categories:
        print(f"Invalid category. Using 'technology' as default.")
        category = 'technology'
    
    max_posts = input("Max posts to scrape (default 30): ").strip()
    max_posts = int(max_posts) if max_posts.isdigit() else 30
    
    print()
    print(f"Starting scrape for category: {category}")
    print(f"Max posts: {max_posts}")
    print("-" * 80)
    print()
    
    try:
        # Initialize scraper with context manager for automatic cleanup
        with FacebookScraper(headless=False, debug=True) as scraper:
            
            # Login to Facebook
            print("Logging in to Facebook...")
            if not scraper.login():
                print("\n❌ Login failed.")
                print("\nPossible reasons:")
                print("  • Invalid credentials in .env file")
                print("  • Facebook security checkpoint (already handled if browser is visible)")
                print("  • 2FA enabled (complete verification in browser)")
                print("  • Facebook detected automation")
                print("\nTip: If you see a checkpoint page, complete the verification in the browser window.")
                return 1
            
            print("✓ Login successful")
            print()
            
            # Get top 10 trending hashtags
            print(f"Scraping top 10 hashtags for {category}...")
            results = scraper.get_top_10_trending(category, max_posts)
            
            if not results:
                print("❌ No results found")
                return 1
            
            print()
            print("=" * 80)
            print(f"TOP 10 TRENDING HASHTAGS - {category.upper()}")
            print("=" * 80)
            print()
            
            # Display results
            for i, hashtag in enumerate(results, 1):
                print(f"{i}. #{hashtag['hashtag']}")
                print(f"   Trending Score: {hashtag['trending_score']}/100")
                print(f"   Engagement Score: {hashtag['engagement_score']}/10")
                print(f"   Posts: {hashtag['post_count']}")
                print(f"   Avg Engagement: {int(hashtag['avg_engagement']):,}")
                print(f"   Sentiment: {hashtag['sentiment']} ({hashtag['sentiment_score']:+.2f})")
                print(f"   Metrics: {int(hashtag['avg_likes']):,} likes, "
                      f"{int(hashtag['avg_comments']):,} comments, "
                      f"{int(hashtag['avg_shares']):,} shares")
                if hashtag.get('is_estimated'):
                    print(f"   ⚠️  Estimated metrics")
                print()
            
            # Save results with UUID version_id
            version_id = str(uuid.uuid4())
            scraper.save_results(results, category, version_id)
            
            print(f"Version ID: {version_id}")
            
            print("=" * 80)
            print("✓ Results saved:")
            print(f"  - JSON file in data/ directory")
            print(f"  - Supabase database (if configured)")
            print(f"  - Logs in logs/scraper.log")
            print("=" * 80)
            
            return 0
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
