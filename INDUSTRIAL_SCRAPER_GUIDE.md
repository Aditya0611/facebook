# Industrial Scraper Guide

## Overview

The Industrial Facebook Scraper (`industrial_scraper.py`) is a production-grade scraper designed for unlimited, self-hosted scraping without relying on third-party credits or APIs.

## Why Industrial Scraper?

- ✅ **No Credit Limits**: Self-hosted, unlimited usage
- ✅ **Production Ready**: Built for industrial-scale operations
- ✅ **Advanced Features**: Rate limiting, proxy management, session persistence
- ✅ **Anti-Detection**: Advanced fingerprinting evasion
- ✅ **Monitoring**: Real-time metrics and statistics

## Quick Start

```python
from industrial_scraper import create_industrial_scraper
import uuid

# Create scraper
scraper = create_industrial_scraper(
    headless=True,
    rate_limit_per_minute=30,
    use_proxies=True,
    use_sessions=True
)

# Use scraper
with scraper:
    if scraper.login():
        results = scraper.get_top_10_trending('technology', max_posts=100)
        scraper.save_results(results, 'technology', str(uuid.uuid4()))
        
        # Get metrics
        metrics = scraper.get_metrics()
        print(f"Success rate: {metrics['success_rate']:.2f}%")
```

## Key Components

### 1. Rate Limiter (Token Bucket Algorithm)

Prevents rate limiting and detection by intelligently throttling requests.

```python
# Automatically handles rate limiting
scraper.navigate_to("https://www.facebook.com")
# Rate limiter ensures requests stay within limits
```

**Features:**
- Token bucket algorithm
- Configurable requests per minute
- Automatic backoff
- Burst support

### 2. Enhanced Proxy Manager

Manages proxy rotation with health checks and automatic recovery.

```python
# Configure proxies in .env
PROXIES=http://proxy1:8080,http://proxy2:8080,http://proxy3:8080

# Proxy manager automatically:
# - Rotates proxies based on success rates
# - Marks dead proxies
# - Recovers failed proxies
# - Tracks statistics
```

**Features:**
- Health checks
- Automatic rotation
- Success rate tracking
- Dead proxy detection
- Auto-recovery

### 3. Session Manager

Persists cookies and sessions to avoid repeated logins.

```python
# Sessions are automatically saved and loaded
# No need to login every time
```

**Features:**
- Cookie persistence
- Session TTL
- Automatic rotation
- Recovery on failure

### 4. Anti-Detection

Advanced fingerprinting evasion to avoid detection.

**Features:**
- Random user agent rotation
- Viewport randomization
- Timezone randomization
- Language randomization
- Stealth JavaScript injection
- Human-like delays
- Mouse movement simulation

### 5. Metrics & Monitoring

Real-time statistics for monitoring performance.

```python
metrics = scraper.get_metrics()

# Available metrics:
# - total_requests
# - successful_requests
# - failed_requests
# - success_rate
# - avg_response_time
# - proxy_stats
# - uptime
# - posts_scraped
# - hashtags_found
```

## Configuration

### Environment Variables (.env)

```env
# Required
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password

# Optional: Proxy list
PROXIES=http://proxy1:8080,http://proxy2:8080

# Optional: Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_key
```

### Industrial Config (config/industrial_config.json)

```json
{
  "scraper": {
    "rate_limit_per_minute": 30,
    "max_concurrent": 1
  },
  "proxy": {
    "enabled": true,
    "health_check_interval": 300,
    "max_failures": 3
  },
  "session": {
    "enabled": true,
    "ttl_seconds": 3600
  }
}
```

## Best Practices

### 1. Rate Limiting
- Start with 30 requests/minute
- Increase gradually if needed
- Monitor for rate limit hits

### 2. Proxy Management
- Use multiple proxies for better reliability
- Monitor proxy health statistics
- Replace dead proxies regularly

### 3. Session Management
- Enable session persistence
- Set appropriate TTL (1 hour default)
- Clean up expired sessions

### 4. Anti-Detection
- Keep all anti-detection features enabled
- Use random delays
- Rotate fingerprints regularly

### 5. Monitoring
- Track success rates
- Monitor proxy performance
- Alert on high failure rates

## Troubleshooting

### High Failure Rate
- Check proxy health
- Reduce rate limit
- Verify credentials
- Check network connectivity

### Rate Limit Hits
- Reduce requests per minute
- Increase delays between requests
- Use more proxies

### Proxy Issues
- Verify proxy URLs
- Check proxy authentication
- Monitor proxy statistics
- Replace dead proxies

### Session Issues
- Clear expired sessions
- Check session directory permissions
- Verify cookie format

## Performance Tuning

### For High Volume
```python
scraper = create_industrial_scraper(
    rate_limit_per_minute=60,  # Higher rate
    use_proxies=True,           # Essential
    use_sessions=True,          # Reduces logins
    max_concurrent=3            # Parallel scraping
)
```

### For Stealth
```python
scraper = create_industrial_scraper(
    rate_limit_per_minute=15,  # Lower rate
    use_proxies=True,          # Essential
    use_sessions=True,         # Reduces logins
    max_concurrent=1           # Sequential
)
```

## Comparison: Standard vs Industrial

| Feature | Standard | Industrial |
|---------|----------|------------|
| Rate Limiting | Basic | Token Bucket |
| Proxy Management | Simple | Health Checks + Auto-Recovery |
| Session Management | None | Persistence + Rotation |
| Anti-Detection | Basic | Advanced Fingerprinting |
| Metrics | Logging | Real-time Statistics |
| Production Ready | ✅ | ✅✅ |
| Scalability | Single | Multi-threaded |

## Examples

### Basic Usage
```python
from industrial_scraper import create_industrial_scraper

scraper = create_industrial_scraper()
with scraper:
    if scraper.login():
        results = scraper.get_top_10_trending('technology')
        scraper.save_results(results, 'technology', 'v1.0')
```

### With Custom Settings
```python
scraper = create_industrial_scraper(
    headless=True,
    debug=False,
    rate_limit_per_minute=45,
    use_proxies=True,
    use_sessions=True,
    max_concurrent=2
)
```

### Monitoring Metrics
```python
with scraper:
    # ... scraping operations ...
    
    metrics = scraper.get_metrics()
    print(f"Success Rate: {metrics['success_rate']:.2f}%")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Proxy Health: {metrics['proxy_stats']['healthy_proxies']}")
```

## Support

For issues or questions:
1. Check logs in `logs/scraper.log`
2. Review metrics for performance issues
3. Verify configuration in `.env` and `config/industrial_config.json`
4. Check proxy health statistics

---

**Ready for industrial-scale scraping!** 🚀

