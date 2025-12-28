@echo off
echo ================================================================
echo Starting DEARS - Distributed Emergency Alert and Response System
echo ================================================================
echo.

echo [1/2] Starting Server Services (Dispatcher, Police, Fire, Medical)...
echo Dispatcher will run on Port 8001.
start "DEARS Services" cmd /k "cd app\servers && set DISPATCHER_PORT=8001 && python run_all_services.py"

timeout /t 5 /nobreak > nul

echo [2/2] Starting Django Client Application...
start "DEARS Client" cmd /k "cd app\client && python manage.py runserver"

echo.
echo ================================================================
echo All DEARS services are starting!
echo ================================================================
echo.
echo Services:
echo   - Dispatcher:   http://localhost:8001 (Backend API)
echo   - Police:       Port 9001
echo   - Fire:         Port 9002
echo   - Medical:      Port 9003
echo   - Django Client: http://localhost:8000 (Web Interface)
echo.
echo Check the opened windows for status and logs.
echo Close this window (services will keep running in their own windows)
echo.
pause
