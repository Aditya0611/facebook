#!/bin/bash
echo "========================================"
echo "Installing Perfect Scraper Dependencies"
echo "========================================"
echo ""

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Installing facebook-scraper..."
python -m pip install facebook-scraper --no-deps
python -m pip install dateparser demjson3 requests-html textblob python-dotenv tenacity

echo ""
echo "========================================"
echo "Testing installation..."
echo "========================================"
python -c "from facebook_scraper import get_posts; print('SUCCESS: facebook-scraper is working!')"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Installation successful!"
    echo "Run: python perfect_demo.py"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Installation may have issues."
    echo "Try: python perfect_demo.py"
    echo "========================================"
fi

