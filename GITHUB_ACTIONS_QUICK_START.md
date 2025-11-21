# GitHub Actions Quick Start

## ✅ What's Been Set Up

1. **Workflow File**: `.github/workflows/scraper.yml`
   - Runs every 4 hours automatically
   - Can be triggered manually
   - Processes all 8 categories

2. **Automated Script**: `automated_scraper.py`
   - Non-interactive version for CI/CD
   - Runs all categories automatically
   - No prompts required

3. **Documentation**: `.github/GITHUB_ACTIONS_SETUP.md`
   - Complete setup guide
   - Troubleshooting tips

## 🚀 Next Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Add GitHub Actions workflow for automated scraping"
git push origin main
```

### 2. Add GitHub Secrets

Go to: **https://github.com/Aditya0611/facebook/settings/secrets/actions**

Add these 4 required secrets:

| Secret Name | Value |
|------------|-------|
| `FACEBOOK_EMAIL` | Your Facebook email |
| `FACEBOOK_PASSWORD` | Your Facebook password |
| `SUPABASE_URL` | Your Supabase URL |
| `SUPABASE_ANON_KEY` | Your Supabase anonymous key |

### 3. Test the Workflow

1. Go to: **https://github.com/Aditya0611/facebook/actions**
2. Click **Facebook Scraper - Scheduled Run**
3. Click **Run workflow** → **Run workflow**

### 4. Monitor Results

- **View runs**: https://github.com/Aditya0611/facebook/actions
- **Download data**: Click on a run → **Artifacts** → Download `scraped-data`
- **View logs**: Click on a run → Click on the **scrape** job

## 📅 Schedule

The scraper runs automatically:
- **Every 4 hours** (00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC)
- **Manual trigger**: Available anytime via Actions tab

## 📊 What Gets Scraped

All 8 categories from `config/categories.json`:
1. technology
2. business
3. health
4. food
5. travel
6. fashion
7. entertainment
8. sports

## 📁 Output

- **JSON files**: `data/facebook_top10_*.json`
- **Logs**: `logs/scraper.log`
- **Supabase**: Data automatically uploaded to database
- **GitHub Artifacts**: Available for 30 days

## ⚙️ Customization

Edit `.github/workflows/scraper.yml` to:
- Change schedule (cron expression)
- Adjust timeout
- Modify max posts per category
- Enable/disable auto-commit

## 🔧 Troubleshooting

See `.github/GITHUB_ACTIONS_SETUP.md` for detailed troubleshooting guide.

## 📝 Notes

- Workflow runs in **headless mode** (no browser UI)
- All 8 categories processed sequentially
- 30-second delay between categories
- Results committed back to repo (optional)
- Artifacts retained for 30 days

