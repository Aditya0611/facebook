#!/usr/bin/env python3
"""
Automated Facebook Scraper - For CI/CD
=======================================
Non-interactive version for GitHub Actions
Runs all categories automatically without prompts
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from industrial_scraper import IndustrialFacebookScraper, create_industrial_scraper

def load_categories():
    """Load all categories from config file"""
    config_path = Path(__file__).parent / "config" / "categories.json"
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return []
    
    with open(config_path, 'r', encoding='utf-8') as f:
        categories_data = json.load(f)
    
    return list(categories_data.keys())

def main():
    """Run automated scraping for ALL categories (non-interactive)"""
    
    print("=" * 80)
    print("Automated Facebook Scraper - GitHub Actions")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load all categories
    all_categories = load_categories()
    if not all_categories:
        print("❌ No categories found in config/categories.json")
        return 1
    
    print(f"Found {len(all_categories)} categories: {', '.join(all_categories)}")
    print()
    
    # Configuration (non-interactive defaults)
    categories = all_categories
    max_posts = int(os.getenv('MAX_POSTS', '100'))
    use_proxies = os.getenv('USE_PROXIES', 'false').lower() == 'true'
    use_sessions = True
    rate_limit = int(os.getenv('RATE_LIMIT', '30'))
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    
    print("Configuration:")
    print(f"  Categories: {len(categories)} ({', '.join(categories)})")
    print(f"  Max posts per category: {max_posts}")
    print(f"  Proxies: {'Enabled' if use_proxies else 'Disabled'}")
    print(f"  Sessions: {'Enabled' if use_sessions else 'Disabled'}")
    print(f"  Rate limit: {rate_limit} requests/minute")
    print(f"  Headless: {headless}")
    print(f"  Estimated time: ~{len(categories) * 10} minutes")
    print("-" * 80)
    print()
    print("Starting scraping process...")
    print("=" * 80)
    print()
    
    try:
        # Create industrial scraper
        scraper = create_industrial_scraper(
            headless=headless,
            debug=True,
            rate_limit_per_minute=rate_limit,
            use_proxies=use_proxies,
            use_sessions=use_sessions,
            max_concurrent=1
        )
        
        with scraper:
            # Login once for all categories
            print("Logging in to Facebook...")
            if not scraper.login():
                print("\n❌ Login failed. Check credentials in environment variables")
                return 1
            
            print("✓ Login successful")
            print()
            
            # Track overall results
            all_results = {}
            start_time = datetime.now()
            successful_categories = 0
            failed_categories = 0
            
            # Process each category
            for idx, category in enumerate(categories, 1):
                print("=" * 80)
                print(f"CATEGORY {idx}/{len(categories)}: {category.upper()}")
                print("=" * 80)
                print()
                
                try:
                    # Scrape category
                    print(f"Scraping top 10 hashtags for {category}...")
                    results = scraper.scrape_category_hashtags(
                        category=category,
                        max_posts=max_posts
                    )
                    
                    if results and len(results) > 0:
                        all_results[category] = results
                        successful_categories += 1
                        print(f"✓ Category '{category}' completed: {len(results)} hashtags found")
                    else:
                        failed_categories += 1
                        print(f"⚠ Category '{category}' completed but no results found")
                    
                    # Delay between categories to avoid rate limiting
                    if idx < len(categories):
                        print(f"\nWaiting 30 seconds before next category...")
                        import time
                        time.sleep(30)
                    
                except Exception as e:
                    failed_categories += 1
                    print(f"❌ Error scraping category '{category}': {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Final summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print()
            print("=" * 80)
            print("SCRAPING SESSION COMPLETE")
            print("=" * 80)
            print(f"Total Categories: {len(categories)}")
            print(f"Successful: {successful_categories}")
            print(f"Failed: {failed_categories}")
            print(f"Total Duration: {duration/60:.1f} minutes")
            print()
            
            # Display metrics
            metrics = scraper.get_metrics()
            print("Final Metrics:")
            print(f"  Total Requests: {metrics.total_requests}")
            print(f"  Successful: {metrics.successful_requests}")
            print(f"  Failed: {metrics.failed_requests}")
            print(f"  Success Rate: {metrics.success_rate:.2f}%")
            print(f"  Total Posts Scraped: {metrics.total_posts_scraped}")
            print(f"  Total Hashtags Found: {metrics.total_hashtags_found}")
            print(f"  Avg Response Time: {metrics.avg_response_time:.2f}s")
            print()
            
            return 0 if failed_categories == 0 else 1
            
    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

