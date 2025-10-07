@echo off
echo Starting Human Body Measurements API with Docker...
echo.

REM Check if Docker is running
docker version >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Start services with Docker Compose
echo Starting services with Docker Compose...
docker-compose up -d

echo.
echo Services started successfully!
echo.
echo API Documentation: http://localhost:8000/docs
echo API Base URL: http://localhost:8000
echo.
echo To stop the services, run: docker-compose down
echo.

pause

