@echo off
echo Starting Human Body Measurements API...
echo.

REM Check if virtual environment exists
if not exist "venv_py37\Scripts\activate.bat" (
    echo Virtual environment not found. Please run the setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv_py37\Scripts\activate.bat

REM Check if Redis is running
echo Checking Redis connection...
python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); r.ping()" 2>nul
if errorlevel 1 (
    echo Redis is not running. Please start Redis first.
    echo You can start Redis with: docker run -d -p 6379:6379 redis:7-alpine
    pause
    exit /b 1
)

REM Start the API
echo Starting API server...
cd api
python start.py

pause

