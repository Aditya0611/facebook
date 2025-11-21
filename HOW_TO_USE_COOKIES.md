# How to Use Cookies for Better Facebook Scraping

## Why Cookies?

Facebook requires authentication to access most content. Without cookies, you'll get 404 errors. With cookies, the scraper can access:
- ✅ Hashtag pages
- ✅ Search results  
- ✅ More posts
- ✅ Better data quality

## Quick Setup

### Step 1: Export Cookies from Browser

**Option A: Using Browser Extension (Easiest)**

1. Install "Get cookies.txt LOCALLY" extension:
   - Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   - Firefox: https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/

2. Go to https://www.facebook.com and log in

3. Click the extension icon → Export → Save as `cookies.txt`

**Option B: Manual Export (Advanced)**

1. Log in to Facebook in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → https://www.facebook.com
4. Copy all cookies and save as `cookies.txt` (Netscape format)

### Step 2: Add to Project

1. Save `cookies.txt` in your project root:
   ```
   facebook_scraper/
   ├── cookies.txt
   ├── perfect_scraper.py
   └── ...
   ```

2. Set in `.env` file:
   ```env
   FACEBOOK_COOKIES_FILE=cookies.txt
   ```

### Step 3: Run Scraper

```bash
python perfect_demo.py
```

## Format of cookies.txt

The file should look like this (Netscape format):
```
# Netscape HTTP Cookie File
.facebook.com	TRUE	/	FALSE	1735689600	c_user	1234567890
.facebook.com	TRUE	/	FALSE	1735689600	xs	abc123def456...
```

## Troubleshooting

### Cookies Not Working?

1. **Check file path**: Make sure `cookies.txt` is in project root
2. **Check format**: Must be Netscape format
3. **Check expiration**: Cookies expire - export fresh ones
4. **Check login**: Make sure you're logged in when exporting

### Still Getting 404 Errors?

1. Export fresh cookies (they expire)
2. Make sure you're logged in when exporting
3. Try using the browser extension method (more reliable)

## Benefits

With cookies:
- ✅ Access to hashtag pages
- ✅ Better search results
- ✅ More posts scraped
- ✅ Higher success rate

Without cookies:
- ❌ 404 errors
- ❌ Limited access
- ❌ Fewer posts

## Security Note

⚠️ **Never commit cookies.txt to git!**

Add to `.gitignore`:
```
cookies.txt
*.txt
!requirements.txt
```

---

**After setting up cookies, run `python perfect_demo.py` again!**

