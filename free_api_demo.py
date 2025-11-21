#!/usr/bin/env python3
"""
Free API Facebook Scraper Demo
==============================

Demonstrates free third-party APIs for Facebook scraping:
1. facebook-scraper (kevinzg) - Completely free, open-source
2. Facebook Graph API - Official API (limited)
3. Crawlbase - 1,000 free requests

Usage:
------
    python free_api_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from free_api_scraper import create_free_api_scraper

def main():
    print("=" * 80)
    print("Free Third-Party API Facebook Scraper Demo")
    print("=" * 80)
    print()
    print("Available APIs:")
    print("  1. facebook-scraper (kevinzg) - Completely FREE, open-source")
    print("  2. Facebook Graph API - Official API (limited, free)")
    print("  3. Crawlbase - 1,000 free requests")
    print()
    
    # Select API type
    print("Select API type:")
    print("  1. facebook-scraper (recommended - completely free)")
    print("  2. Facebook Graph API (official, limited)")
    print("  3. Crawlbase (1,000 free requests)")
    
    choice = input("\nEnter choice (1-3, default 1): ").strip() or "1"
    
    api_map = {
        "1": "facebook_scraper",
        "2": "graph_api",
        "3": "crawlbase"
    }
    
    api_type = api_map.get(choice, "facebook_scraper")
    
    # Category
    category = input("\nEnter category (technology/business/health/food): ").strip().lower() or "technology"
    
    print()
    print(f"Using API: {api_type}")
    print(f"Category: {category}")
    print("-" * 80)
    print()
    
    try:
        # Create scraper
        scraper = create_free_api_scraper(api_type=api_type)
        
        # Get trending hashtags
        print(f"Scraping trending hashtags for {category}...")
        results = scraper.get_trending_hashtags(category, max_posts=50)
        
        if not results:
            print("❌ No results found")
            print("\nTips:")
            print("  - For facebook-scraper: Install with 'pip install facebook-scraper'")
            print("  - For Graph API: Set FACEBOOK_APP_ID and FACEBOOK_APP_SECRET in .env")
            print("  - For Crawlbase: Set CRAWLBASE_API_TOKEN in .env (get from crawlbase.com)")
            return 1
        
        # Display results
        print()
        print("=" * 80)
        print(f"TOP TRENDING HASHTAGS - {category.upper()}")
        print("=" * 80)
        print()
        
        for i, hashtag in enumerate(results, 1):
            print(f"{i}. #{hashtag['hashtag']}")
            print(f"   Trending Score: {hashtag['trending_score']:.1f}/100")
            print(f"   Engagement Score: {hashtag['engagement_score']:.1f}/10")
            print(f"   Posts: {hashtag['post_count']}")
            print(f"   Avg Engagement: {int(hashtag['avg_engagement']):,}")
            print(f"   Metrics: {int(hashtag['avg_likes']):,} likes, "
                  f"{int(hashtag['avg_comments']):,} comments, "
                  f"{int(hashtag['avg_shares']):,} shares")
            print(f"   Sentiment: {hashtag['sentiment']} ({hashtag['sentiment_score']:+.2f})")
            print()
        
        # Save results
        scraper.save_results(results, category)
        
        print("=" * 80)
        print("✓ Results saved to data/ directory")
        print("=" * 80)
        
        return 0
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\nInstall with:")
        if "facebook-scraper" in str(e):
            print("  pip install facebook-scraper")
        elif "requests" in str(e):
            print("  pip install requests")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

