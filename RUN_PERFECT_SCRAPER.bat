@echo off
echo ========================================
echo Perfect Scraper - Quick Start
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
    echo.
) else (
    echo WARNING: Virtual environment not found!
    echo Creating one now...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Check if facebook-scraper is installed
python -c "from facebook_scraper import get_posts" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installing facebook-scraper...
    pip install facebook-scraper textblob
    echo.
)

echo ========================================
echo Running Perfect Scraper...
echo ========================================
echo.

python perfect_demo.py

pause

