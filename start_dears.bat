@echo off
echo ================================================================
echo Starting DEARS - Distributed Emergency Alert and Response System
echo ================================================================
echo.
echo Opening all services in Windows Terminal with tabs...
echo.

REM Get the current directory
set "PROJECT_DIR=%CD%"

REM Start Windows Terminal with multiple tabs - one for each service
wt -w 0 new-tab --title "Dispatcher Service" -d "%PROJECT_DIR%\app\servers\dispatcher_service" cmd /k "python run.py" ; new-tab --title "Police Service" -d "%PROJECT_DIR%\app\servers\response_services\police_service" cmd /k "python run.py" ; new-tab --title "Fire Service" -d "%PROJECT_DIR%\app\servers\response_services\fire_service" cmd /k "python run.py" ; new-tab --title "Medical Service" -d "%PROJECT_DIR%\app\servers\response_services\medical_service" cmd /k "python run.py" ; new-tab --title "Django Client" -d "%PROJECT_DIR%\app\client" cmd /k "python manage.py runserver"

echo.
echo ================================================================
echo All DEARS services are starting in Windows Terminal!
echo ================================================================
echo.
echo Services (each in its own tab):
echo   - Tab 1: Dispatcher Service (http://localhost:8001)
echo   - Tab 2: Police Service (Port 9001)
echo   - Tab 3: Fire Service (Port 9002)
echo   - Tab 4: Medical Service (Port 9003)
echo   - Tab 5: Django Client (http://localhost:8000)
echo.
echo All services are running in separate tabs in ONE Windows Terminal window.
echo You can close this window now.
echo.
pause
