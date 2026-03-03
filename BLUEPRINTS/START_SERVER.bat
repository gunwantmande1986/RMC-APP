@echo off
echo.
echo ========================================
echo    RMC ERP - FLASK SERVER STARTER
echo ========================================
echo.
echo Starting Flask server on http://localhost:8080
echo.
echo Press Ctrl+C to stop server
echo.

cd /d "%~dp0\..\..\SKCON RMC WEB APP"
start "SKCON RMC Server" python app.py

timeout /t 5 /nobreak >nul
start "" "http://localhost:8080"

echo.
echo Server is running! Don't close this window.
pause
