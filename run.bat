@echo off
cd /d "%~dp0"
echo =========================================
echo  🛡️ Cyber Shield SIEM - Starting...
echo =========================================
echo.
echo 🌐 Dashboard will open at: http://localhost:5000
echo.
call venv\Scripts\activate.bat
start "" http://localhost:5000
python run.py
pause
