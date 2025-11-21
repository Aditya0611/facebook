@echo off
echo ========================================
echo Installing Perfect Scraper Dependencies
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Installing facebook-scraper...
python -m pip install facebook-scraper --no-deps
python -m pip install dateparser demjson3 requests-html textblob python-dotenv tenacity

echo.
echo ========================================
echo Testing installation...
echo ========================================
python -c "from facebook_scraper import get_posts; print('SUCCESS: facebook-scraper is working!')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Installation successful!
    echo Run: python perfect_demo.py
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Installation may have issues.
    echo Try: python perfect_demo.py
    echo ========================================
)

pause

