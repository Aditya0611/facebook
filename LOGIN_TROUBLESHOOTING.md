# Facebook Login Troubleshooting Guide

## Issue: Login Failing in GitHub Actions

Your scraper is failing to log in to Facebook. The error shows:
```
Login failed - redirected to login page
```

## Common Causes

### 1. **Facebook Detecting Automation** ⚠️ MOST COMMON
- Facebook blocks automated logins, especially in headless mode
- GitHub Actions runs in headless mode, which is easier to detect
- Facebook may require additional verification (2FA, checkpoint)

### 2. **Incorrect Credentials**
- Email or password wrong in GitHub Secrets
- Password changed since adding to secrets

### 3. **2FA Enabled**
- Two-Factor Authentication requires manual input
- Can't be handled automatically in headless mode

### 4. **Security Checkpoint**
- Facebook may require security verification
- Requires manual intervention (not possible in headless mode)

## Solutions

### Solution 1: Verify GitHub Secrets ✅ (First Step)

1. Go to your repository: https://github.com/Aditya0611/facebook
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Verify these secrets exist and are correct:
   - `FACEBOOK_EMAIL` - Your Facebook email
   - `FACEBOOK_PASSWORD` - Your Facebook password

4. **Test credentials manually**:
   - Open https://www.facebook.com in a browser
   - Try logging in with the same credentials
   - If login fails, credentials are wrong

### Solution 2: Disable 2FA Temporarily ⚠️

If you have 2FA enabled:

1. Go to Facebook Settings → Security and Login
2. **Temporarily disable 2FA** for testing
3. Try running the scraper again
4. Re-enable 2FA after testing

**⚠️ WARNING**: Disabling 2FA reduces security. Only do this temporarily for testing.

### Solution 3: Use App-Specific Password (If Available)

Some Facebook accounts support app-specific passwords:

1. Go to Facebook Settings → Security and Login
2. Look for "App Passwords" section
3. Generate an app-specific password
4. Use this password in GitHub Secrets instead of your main password

### Solution 4: Run in Non-Headless Mode (For Local Testing)

For local testing, you can see what's happening:

1. Edit `.github/workflows/scraper.yml`
2. Add environment variable:
   ```yaml
   - name: Run Facebook Scraper
     env:
       HEADLESS: false  # Enable this for debugging
     run: |
       python automated_scraper.py
   ```

**⚠️ NOTE**: Non-headless mode won't work in GitHub Actions, but you can test locally.

### Solution 5: Use Session Cookies Instead (Alternative Approach)

Instead of automatic login, you can use saved session cookies:

1. **Export cookies from your browser**:
   - Install browser extension: "Get cookies.txt LOCALLY"
   - Log in to Facebook manually
   - Export cookies as `cookies.txt`
   - Upload to a secure location (encrypted)

2. **Load cookies in scraper**:
   - Modify scraper to load cookies instead of logging in
   - More reliable but requires manual cookie refresh

### Solution 6: Use a Different Account (Recommended for Testing)

Create a test Facebook account:

1. Create a new Facebook account (test account)
2. Add it to GitHub Secrets
3. Use this account for automated scraping
4. Less risk to your main account

### Solution 7: Reduce Detection Signals

Make the scraper look more human-like:

1. **Add delays**: Already implemented (30 seconds between categories)
2. **Use residential proxies**: If available
3. **Rotate user agents**: Already implemented
4. **Limit frequency**: Run less often (e.g., daily instead of every 3 hours)

## Quick Diagnostic Steps

1. ✅ **Check if credentials are set**:
   ```bash
   # In GitHub Actions, add debug step:
   echo "Email set: $([ -n "$FACEBOOK_EMAIL" ] && echo 'YES' || echo 'NO')"
   echo "Password set: $([ -n "$FACEBOOK_PASSWORD" ] && echo 'YES' || echo 'NO')"
   ```

2. ✅ **Test login manually**:
   - Log in with same credentials in a browser
   - Check if it works
   - Check for any security prompts

3. ✅ **Check Facebook security settings**:
   - Review recent login attempts
   - Check for security alerts
   - Verify account is not locked

## Next Steps

1. **First**: Verify credentials in GitHub Secrets are correct
2. **Second**: Test login manually with same credentials
3. **Third**: Check if 2FA is enabled and consider disabling temporarily
4. **Fourth**: Consider using a test account for automation

## Alternative: Use Free API Instead

If login continues to fail, consider using the free API scraper (`free_api_scraper.py`) which doesn't require login.

---

**Current Status**: Login is failing because Facebook is blocking automated login attempts. This is expected behavior for automated tools.

