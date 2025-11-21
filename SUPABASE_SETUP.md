# Supabase Setup Guide 🗄️

## Step-by-Step Setup

### 1. Create Supabase Account & Project

1. **Go to Supabase**: https://supabase.com
2. **Sign up** (free tier available)
3. **Create a new project**:
   - Click "New Project"
   - Enter project name (e.g., "facebook-scraper")
   - Enter database password (save it!)
   - Select region closest to you
   - Click "Create new project"
   - Wait 2-3 minutes for setup

### 2. Get Your Credentials

1. **Go to Project Settings**:
   - Click ⚙️ (Settings) in left sidebar
   - Click "API" in settings menu

2. **Copy Your Credentials**:
   - **Project URL**: Under "Project URL"
     - Example: `https://abcdefghijklmnop.supabase.co`
   - **Anon/Public Key**: Under "Project API keys" → "anon public"
     - This is your `SUPABASE_ANON_KEY`

### 3. Create the Database Table

1. **Go to SQL Editor**:
   - Click "SQL Editor" in left sidebar
   - Click "New query"

2. **Run This SQL**:
   ```sql
   -- Create facebook table for storing hashtag trends
   CREATE TABLE IF NOT EXISTS facebook (
     id BIGSERIAL PRIMARY KEY,
     platform TEXT NOT NULL DEFAULT 'Facebook',
     topic_hashtag TEXT NOT NULL,
     engagement_score FLOAT NOT NULL,
     sentiment_polarity FLOAT NOT NULL,
     sentiment_label TEXT NOT NULL,
     posts INTEGER NOT NULL,
     views BIGINT NOT NULL,
     version_id TEXT NOT NULL,
     metadata JSONB DEFAULT '{}'::jsonb,
     created_at TIMESTAMPTZ DEFAULT NOW(),
     updated_at TIMESTAMPTZ DEFAULT NOW()
   );

   -- Create indexes for faster queries
   CREATE INDEX IF NOT EXISTS idx_facebook_topic_hashtag ON facebook(topic_hashtag);
   CREATE INDEX IF NOT EXISTS idx_facebook_version_id ON facebook(version_id);
   CREATE INDEX IF NOT EXISTS idx_facebook_created_at ON facebook(created_at);
   CREATE INDEX IF NOT EXISTS idx_facebook_engagement_score ON facebook(engagement_score DESC);

   -- Enable Row Level Security (RLS) - optional but recommended
   ALTER TABLE facebook ENABLE ROW LEVEL SECURITY;

   -- Create policy to allow all operations (adjust as needed)
   CREATE POLICY "Allow all operations" ON facebook
     FOR ALL
     USING (true)
     WITH CHECK (true);
   ```

3. **Click "Run"** to execute the SQL

### 4. Configure Your .env File

1. **Create/Edit `.env` file** in your project root:
   ```env
   # Facebook Credentials
   FACEBOOK_EMAIL=your-email@example.com
   FACEBOOK_PASSWORD=your-password

   # Supabase Configuration
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-anon-key-here
   ```

2. **Replace with your actual values**:
   - `SUPABASE_URL`: Your project URL from step 2
   - `SUPABASE_ANON_KEY`: Your anon key from step 2

### 5. Verify Setup

Run this test script to verify everything works:

```python
# test_supabase.py
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

if not url or not key:
    print("❌ Supabase credentials not found in .env")
    exit(1)

try:
    supabase = create_client(url, key)
    
    # Test insert
    test_record = {
        'platform': 'Facebook',
        'topic_hashtag': 'test_hashtag',
        'engagement_score': 8.5,
        'sentiment_polarity': 0.65,
        'sentiment_label': 'positive',
        'posts': 10,
        'views': 1000,
        'version_id': 'test-version-123',
        'metadata': {
            'category': 'technology',
            'trending_score': 85.0
        }
    }
    
    response = supabase.table('facebook').insert(test_record).execute()
    print("✅ Supabase connection successful!")
    print(f"✅ Test record inserted: {response.data}")
    
    # Test query
    result = supabase.table('facebook').select('*').eq('version_id', 'test-version-123').execute()
    print(f"✅ Query successful: Found {len(result.data)} records")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
```

Run it:
```bash
python test_supabase.py
```

---

## Table Schema

### Main Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Auto-incrementing primary key |
| `platform` | TEXT | Platform name (default: "Facebook") |
| `topic_hashtag` | TEXT | The hashtag name |
| `engagement_score` | FLOAT | Engagement score (0-10) |
| `sentiment_polarity` | FLOAT | Sentiment (-1 to +1) |
| `sentiment_label` | TEXT | "positive", "negative", "neutral" |
| `posts` | INTEGER | Number of posts analyzed |
| `views` | BIGINT | Total engagement/views |
| `version_id` | TEXT | Unique version identifier |
| `metadata` | JSONB | Additional data (category, trending_score, etc.) |
| `created_at` | TIMESTAMPTZ | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

### Metadata JSON Structure

The `metadata` column contains:
```json
{
  "category": "technology",
  "trending_score": 97.4,
  "avg_engagement": 573.5,
  "likes": 450,
  "comments": 90,
  "shares": 33,
  "avg_likes": 450.0,
  "avg_comments": 90.0,
  "avg_shares": 33.0,
  "hashtag_url": "https://www.facebook.com/hashtag/technology",
  "language": "en",
  "is_estimated": false,
  "confidence_score": 1.0
}
```

---

## Querying Your Data

### Using Supabase Dashboard

1. Go to **Table Editor** → **facebook**
2. View all records
3. Filter, sort, and search

### Using SQL

```sql
-- Get latest hashtags
SELECT * FROM facebook 
ORDER BY created_at DESC 
LIMIT 10;

-- Get hashtags by category
SELECT * FROM facebook 
WHERE metadata->>'category' = 'technology'
ORDER BY (metadata->>'trending_score')::float DESC;

-- Get top trending hashtags
SELECT 
  topic_hashtag,
  engagement_score,
  (metadata->>'trending_score')::float as trending_score,
  (metadata->>'category') as category
FROM facebook
ORDER BY (metadata->>'trending_score')::float DESC
LIMIT 20;
```

### Using Python

```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_ANON_KEY')
)

# Get latest hashtags
result = supabase.table('facebook')\
    .select('*')\
    .order('created_at', desc=True)\
    .limit(10)\
    .execute()

for record in result.data:
    print(f"#{record['topic_hashtag']}: {record['engagement_score']}/10")
```

---

## Troubleshooting

### "Supabase credentials not found"
- ✅ Check `.env` file exists
- ✅ Check `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set
- ✅ Restart your script after editing `.env`

### "Table 'facebook' does not exist"
- ✅ Run the SQL schema creation script (step 3)
- ✅ Check you're in the correct project

### "Permission denied"
- ✅ Check RLS policies are set correctly
- ✅ Verify your anon key is correct

### "Connection timeout"
- ✅ Check your internet connection
- ✅ Verify SUPABASE_URL is correct
- ✅ Check Supabase project status

---

## Next Steps

1. ✅ Run the scraper - data will auto-save to Supabase
2. ✅ View data in Supabase dashboard
3. ✅ Query data using SQL or API
4. ✅ Build dashboards/analytics on top of data

---

## Security Notes

- **Anon Key**: Safe to use in client-side code
- **Service Role Key**: Keep secret, never expose
- **RLS Policies**: Adjust based on your security needs
- **API Rate Limits**: Free tier has limits, upgrade if needed

---

**Ready to go!** Once configured, your scraper will automatically save all hashtags to Supabase! 🚀

