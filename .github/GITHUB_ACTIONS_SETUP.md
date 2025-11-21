# GitHub Actions Setup Guide

This guide explains how to set up the automated Facebook scraper to run every 4 hours using GitHub Actions.

## Repository
- **Repository Name**: `facebook`
- **Owner**: `Aditya0611`
- **Full URL**: https://github.com/Aditya0611/facebook

## Workflow Details

The workflow (`scraper.yml`) is configured to:
- **Schedule**: Run every 4 hours (cron: `0 */4 * * *`)
- **Timeout**: 120 minutes (2 hours)
- **Platform**: Ubuntu Latest
- **Python Version**: 3.11

## Required GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

2. Add these secrets:

### Required Secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `FACEBOOK_EMAIL` | Your Facebook login email | `your.email@example.com` |
| `FACEBOOK_PASSWORD` | Your Facebook login password | `your_password` |
| `SUPABASE_URL` | Your Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Your Supabase anonymous key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

### Optional Secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `PROXIES` | Proxy list (comma-separated) | `http://proxy1:port,http://proxy2:port` |

## How to Add Secrets

1. Navigate to your repository: https://github.com/Aditya0611/facebook
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Enter the secret name and value
6. Click **Add secret**
7. Repeat for all required secrets

## Workflow Features

### Automatic Execution
- Runs every 4 hours automatically
- Can also be triggered manually via **Actions** tab → **Run workflow**

### Data Storage
- Scraped data saved to `data/*.json` files
- Logs saved to `logs/*.log` files
- Data automatically uploaded as GitHub Artifacts (retained for 30 days)
- Optionally commits results back to repository

### Categories Processed
The scraper processes all 8 categories from `config/categories.json`:
1. technology
2. business
3. health
4. food
5. travel
6. fashion
7. entertainment
8. sports

## Manual Trigger

To manually trigger the workflow:

1. Go to **Actions** tab in your repository
2. Select **Facebook Scraper - Scheduled Run** workflow
3. Click **Run workflow** button
4. Select branch (usually `main` or `master`)
5. Click **Run workflow**

## Monitoring

### View Workflow Runs
- Go to **Actions** tab
- Click on a workflow run to see:
  - Execution logs
  - Success/failure status
  - Duration
  - Artifacts (scraped data)

### View Logs
- Click on a workflow run
- Click on the **scrape** job
- Expand steps to see detailed logs

### Download Artifacts
- Click on a completed workflow run
- Scroll to **Artifacts** section
- Download `scraped-data` to get all JSON files and logs

## Troubleshooting

### Login Failures
- Verify `FACEBOOK_EMAIL` and `FACEBOOK_PASSWORD` secrets are correct
- Facebook may require 2FA - consider using an app-specific password
- Check if Facebook has blocked the account

### Timeout Issues
- Default timeout is 120 minutes
- If all 8 categories take longer, increase timeout in `scraper.yml`:
  ```yaml
  timeout-minutes: 180  # 3 hours
  ```

### Missing Dependencies
- All dependencies are installed automatically
- If issues occur, check the "Install Python dependencies" step logs

### Playwright Browser Issues
- Browsers are installed automatically
- If issues occur, check the "Install Playwright browsers" step logs

## Customization

### Change Schedule
Edit `.github/workflows/scraper.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 0 * * *'     # Daily at midnight
```

### Change Max Posts
Set environment variable in workflow:
```yaml
- name: Run Facebook Scraper
  env:
    MAX_POSTS: '150'
  run: |
    python automated_scraper.py
```

### Disable Auto-Commit
Remove or comment out the "Commit and push results" step in `scraper.yml`

## Security Notes

- **Never commit** `.env` files or credentials to the repository
- All sensitive data should be in GitHub Secrets
- The `.env` file is created dynamically during workflow execution
- It's automatically cleaned up after the workflow completes

## Support

If you encounter issues:
1. Check workflow logs in **Actions** tab
2. Verify all secrets are set correctly
3. Test locally with `python automated_scraper.py`
4. Check Facebook account status

