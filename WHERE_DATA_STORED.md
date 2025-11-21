# Where Hashtags Are Stored 📁

## Storage Locations

Your scraped hashtags are saved in **2 places**:

---

## 1. 📄 Local JSON Files (Always Saved)

### Location
```
data/facebook_top10_{category}_{timestamp}.json
```

### Full Path
```
C:\Users\rajni\OneDrive\Desktop\facebook_scraper\data\
```

### File Format
- **Naming**: `facebook_top10_{category}_{YYYYMMDD}_{HHMMSS}.json`
- **Example**: `facebook_top10_technology_20251114_134634.json`
- **Format**: JSON with 2-space indentation
- **Encoding**: UTF-8

### Example File Structure
```json
[
  {
    "hashtag": "technology",
    "trending_score": 97.4,
    "engagement_score": 6.47,
    "post_count": 28,
    "avg_engagement": 573,
    "sentiment": "positive",
    "sentiment_score": 0.60,
    "avg_likes": 450,
    "avg_comments": 90,
    "avg_shares": 33,
    "category": "technology",
    "version_id": "uuid-here",
    "scraped_at": "2025-11-14T13:46:34",
    ...
  },
  ...
]
```

### How to Access
```bash
# View all files
dir data\*.json

# Open a specific file
notepad data\facebook_top10_technology_20251114_134634.json

# Or use any JSON viewer/editor
```

---

## 2. 🗄️ Supabase Database (Optional)

### Location
- **Table**: `facebook`
- **Schema**: `unified_trend_record`

### Requirements
Add to your `.env` file:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### How to Check if Configured
1. Check `.env` file for `SUPABASE_URL` and `SUPABASE_ANON_KEY`
2. If missing, you'll see in logs:
   ```
   "Supabase credentials not found, skipping upload"
   ```
3. If configured, you'll see:
   ```
   "Supabase upload successful"
   ```

### Accessing Supabase Data
1. Go to your Supabase dashboard
2. Navigate to **Table Editor**
3. Select `facebook` table
4. View all scraped hashtags

---

## 📊 Current Files in Your Data Directory

Based on your current setup, you have:

✅ **Technology**: Multiple files (latest: `20251114_134634.json`)
✅ **Business**: `20251114_141849.json`
✅ **Entertainment**: `20251114_160039.json`
✅ **Fashion**: `20251114_152746.json`
✅ **Food**: `20251114_143104.json`
✅ **Health**: `20251114_142609.json`
✅ **Travel**: `20251114_143936.json`

---

## 🔍 Finding Your Data

### Method 1: File Explorer
1. Open File Explorer
2. Navigate to: `C:\Users\rajni\OneDrive\Desktop\facebook_scraper\data\`
3. All JSON files are there!

### Method 2: Command Line
```bash
# List all JSON files
dir data\*.json

# Count files
dir data\*.json | find /c ".json"

# View latest file
dir data\*.json /O-D
```

### Method 3: Python Script
```python
from pathlib import Path
import json

data_dir = Path("data")
json_files = list(data_dir.glob("facebook_top10_*.json"))

for file in sorted(json_files, reverse=True):  # Latest first
    print(f"\n{file.name}")
    with open(file) as f:
        data = json.load(f)
        print(f"  Hashtags: {len(data)}")
        print(f"  Category: {data[0]['category'] if data else 'N/A'}")
```

---

## 📝 Data Structure

Each JSON file contains an array of hashtag objects with:

- `hashtag` - The hashtag name (without #)
- `trending_score` - Score out of 100
- `engagement_score` - Score out of 10
- `post_count` - Number of posts analyzed
- `avg_engagement` - Average engagement
- `sentiment` - positive/negative/neutral
- `sentiment_score` - Sentiment value (-1 to +1)
- `avg_likes`, `avg_comments`, `avg_shares` - Engagement metrics
- `category` - Category name
- `version_id` - Unique version identifier
- `scraped_at` - Timestamp of scraping

---

## 💡 Tips

1. **Backup**: JSON files are your primary data source - keep them safe!
2. **Version Control**: Each run creates a new file with timestamp
3. **Supabase**: Optional but useful for querying/analyzing across runs
4. **File Size**: Each file is typically 5-20 KB (10 hashtags)

---

## 🚀 Next Steps

1. **View Data**: Open any JSON file in a text editor or JSON viewer
2. **Analyze**: Use Python/pandas to analyze trends over time
3. **API**: Use Supabase API to query data programmatically
4. **Export**: Convert JSON to CSV/Excel for spreadsheet analysis

