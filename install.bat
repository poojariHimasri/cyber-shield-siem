@echo off
cd /d "%~dp0"
echo =========================================
echo  🛡️ Cyber Shield SIEM - Setup
echo =========================================
echo.
echo Creating virtual environment...
C:\Users\pooja\.local\bin\python3.14.exe -m venv venv
echo.
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo =========================================
echo  ✅ Setup complete!
echo.
echo  Run the application with: run.bat
echo =========================================
pause

