# Free Third-Party API Guide

## Overview

This guide covers **completely free** third-party APIs and libraries for Facebook scraping. No credits, no limits (or very generous free tiers).

## 🆓 Free Options

### 1. **facebook-scraper (kevinzg)** ⭐ RECOMMENDED
- **Cost**: 100% FREE (open-source)
- **Limits**: None (self-hosted)
- **Installation**: `pip install facebook-scraper`
- **Best for**: Unlimited scraping, no API keys needed

### 2. **Facebook Graph API** (Official)
- **Cost**: FREE
- **Limits**: Limited public data access
- **Requirements**: Facebook App ID & Secret
- **Best for**: Official integration, limited use cases

### 3. **Crawlbase**
- **Cost**: FREE (1,000 requests)
- **Limits**: 1,000 free requests on signup
- **Requirements**: API token (free signup)
- **Best for**: Quick testing, small projects

### 4. **ScrapeCreators**
- **Cost**: FREE (100 API calls)
- **Limits**: 100 free API calls
- **Requirements**: API key (free signup)
- **Best for**: Very small projects

## Quick Start

### Option 1: facebook-scraper (Recommended)

```bash
# Install
pip install facebook-scraper

# Run demo
python free_api_demo.py
# Select option 1 when prompted
```

**Why it's the best:**
- ✅ Completely free, no credits
- ✅ Open-source (GitHub: kevinzg/facebook-scraper)
- ✅ No API keys required
- ✅ Unlimited usage
- ✅ Actively maintained

### Option 2: Facebook Graph API

```bash
# Setup in .env
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# Run
python free_api_demo.py
# Select option 2
```

**Limitations:**
- Limited public data access
- Requires Facebook App registration
- Most endpoints need user authentication

### Option 3: Crawlbase

```bash
# Sign up at crawlbase.com (free)
# Get API token

# Setup in .env
CRAWLBASE_API_TOKEN=your_token

# Run
python free_api_demo.py
# Select option 3
```

**Free tier:**
- 1,000 requests on signup
- Good for testing

## Usage Examples

### Using facebook-scraper (Free)

```python
from free_api_scraper import create_free_api_scraper

# Create scraper (completely free, no API keys needed)
scraper = create_free_api_scraper(api_type='facebook_scraper')

# Get trending hashtags
results = scraper.get_trending_hashtags('technology', max_posts=50)

# Save results
scraper.save_results(results, 'technology')
```

### Using Facebook Graph API

```python
# Setup in .env first:
# FACEBOOK_APP_ID=your_app_id
# FACEBOOK_APP_SECRET=your_app_secret

scraper = create_free_api_scraper(api_type='graph_api')
results = scraper.get_trending_hashtags('technology')
```

### Using Crawlbase

```python
# Setup in .env first:
# CRAWLBASE_API_TOKEN=your_token

scraper = create_free_api_scraper(api_type='crawlbase')
results = scraper.get_trending_hashtags('technology')
```

## Comparison

| API | Cost | Free Tier | Limits | Setup Difficulty |
|-----|------|-----------|--------|------------------|
| **facebook-scraper** | FREE | Unlimited | None | ⭐ Easy |
| **Graph API** | FREE | Limited | Public data only | ⭐⭐ Medium |
| **Crawlbase** | FREE | 1,000 requests | After free tier | ⭐ Easy |
| **ScrapeCreators** | FREE | 100 calls | After free tier | ⭐ Easy |

## Recommended Setup

### For Unlimited Free Scraping:

1. **Use facebook-scraper** (completely free, no limits)
   ```bash
   pip install facebook-scraper
   python free_api_demo.py
   ```

2. **Optional**: Add cookies file for better access
   - Export cookies from browser
   - Save to `cookies.txt`
   - Set `FACEBOOK_COOKIES_FILE=cookies.txt` in `.env`

### For Official Integration:

1. **Use Facebook Graph API**
   - Register Facebook App
   - Get App ID and Secret
   - Set in `.env`

## Installation

```bash
# Install all free API dependencies
pip install facebook-scraper requests

# Or install from requirements.txt
pip install -r requirements.txt
```

## Configuration (.env)

```env
# Optional: For facebook-scraper (better access)
FACEBOOK_COOKIES_FILE=cookies.txt

# Optional: For Graph API
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# Optional: For Crawlbase
CRAWLBASE_API_TOKEN=your_token
```

## Features

All free API scrapers support:
- ✅ Trending hashtag extraction
- ✅ Sentiment analysis
- ✅ Engagement metrics
- ✅ Category-based scraping
- ✅ JSON output

## Troubleshooting

### facebook-scraper Issues

**Problem**: "No results found"
- **Solution**: Export cookies from browser and use cookies file
- **How**: Use browser extension to export cookies, save as `cookies.txt`

**Problem**: Rate limiting
- **Solution**: Add delays between requests
- **Code**: Already handled in the scraper

### Graph API Issues

**Problem**: "Access token error"
- **Solution**: Verify App ID and Secret in `.env`
- **Check**: Facebook App is active and approved

### Crawlbase Issues

**Problem**: "API token invalid"
- **Solution**: Sign up at crawlbase.com and get new token
- **Check**: Token is set in `.env`

## Best Practices

1. **Start with facebook-scraper** - It's completely free and unlimited
2. **Use cookies file** - Better access, fewer rate limits
3. **Respect rate limits** - Add delays between requests
4. **Monitor usage** - Track API calls for services with limits
5. **Combine approaches** - Use multiple APIs for redundancy

## Cost Comparison

| Solution | Monthly Cost | Limits |
|----------|-------------|--------|
| **facebook-scraper** | $0 | Unlimited |
| **Graph API** | $0 | Limited public data |
| **Crawlbase** | $0 (free tier) | 1,000 requests |
| **Apify** | $0 (free tier) | $5 credits/month |
| **Industrial Scraper** | $0 | Unlimited (self-hosted) |

## Recommendation

**For unlimited free scraping:**
1. Use **facebook-scraper** (completely free, no limits)
2. Or use **Industrial Scraper** (self-hosted, unlimited)

**For quick testing:**
- Use **Crawlbase** (1,000 free requests)

**For official integration:**
- Use **Facebook Graph API** (official, but limited)

---

**Ready to scrape for free!** 🚀

Run `python free_api_demo.py` to get started.

