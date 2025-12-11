@echo off
REM Setup Python virtual environment for Windows

REM Create venv if missing
if not exist .venv (
    python -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo Setup complete! You can now run start_all.bat or activate the venv and run services manually.
