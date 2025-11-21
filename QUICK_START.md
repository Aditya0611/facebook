# Quick Start Guide - Perfect Scraper

## The Problem You're Facing

The Playwright scraper (`industrial_demo.py`) is not finding posts because:
- Facebook's page structure has changed
- Facebook is blocking/redirecting automated searches
- Selectors are outdated

## The Solution: Use Perfect Scraper

The **Perfect Scraper** uses the `facebook-scraper` library which is:
- ✅ More reliable (handles Facebook changes automatically)
- ✅ 100% FREE (unlimited usage)
- ✅ Better at finding posts
- ✅ Perfect for website display

## Quick Setup

### ⚠️ IMPORTANT: Activate Virtual Environment First!

You must activate your virtual environment before running:

**Windows:**
```bash
venv\Scripts\activate
pip install facebook-scraper textblob
python perfect_demo.py
```

**Or use the batch file:**
```bash
RUN_PERFECT_SCRAPER.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
pip install facebook-scraper textblob
python perfect_demo.py
```

### Why?

The `facebook-scraper` was installed in your `venv` folder, but you're running Python from system. You need to activate the virtual environment first!

### 3. Use in Your Code
```python
from perfect_scraper import create_perfect_scraper

# Create scraper (100% free, unlimited)
scraper = create_perfect_scraper()

# Get trending hashtags
results = scraper.get_trending_hashtags('technology', max_posts=100)

# Save results (perfect JSON for your website)
scraper.save_results(results, 'technology')
```

## Why Perfect Scraper Works Better

1. **Uses facebook-scraper library** - Actively maintained, handles Facebook changes
2. **Multiple search strategies** - Tries hashtag pages, search, and popular pages
3. **Better error handling** - Retries with different methods
4. **No browser needed** - Faster and more reliable

## Optional: Add Cookies for Better Access

If you want even better results, export cookies from your browser:

1. Install browser extension (e.g., "Get cookies.txt LOCALLY")
2. Export cookies from facebook.com
3. Save as `cookies.txt`
4. Set in `.env`: `FACEBOOK_COOKIES_FILE=cookies.txt`

## Comparison

| Feature | Industrial Scraper | Perfect Scraper |
|---------|-------------------|-----------------|
| **Finds Posts** | ❌ Struggles | ✅ Works |
| **Cost** | FREE | FREE |
| **Reliability** | Medium | High |
| **Setup** | Complex | Simple |
| **Website Ready** | ✅ | ✅✅ |

## Recommendation

**Use Perfect Scraper for your website!**

It's specifically designed for:
- ✅ Displaying trends on websites
- ✅ Reliable data extraction
- ✅ Clean JSON output
- ✅ 100% free, unlimited usage

Run `python perfect_demo.py` now!

